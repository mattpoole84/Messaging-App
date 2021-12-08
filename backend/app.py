from flask import jsonify,request
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime
from celery import Celery
import mandrill
from twilio.rest import Client as Twilio_Client
from twilio.base.exceptions import TwilioRestException

app = FlaskAPI(__name__)

app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],backend=app.config['CELERY_RESULT_BACKEND'],)


db = SQLAlchemy(app)

mandrill_client = mandrill.Mandrill(app.config['MANDRILL_KEY'])
twilio_client = Twilio_Client(app.config['TWILIO_ACCOUNT_SID'],app.config['TWILIO_AUTH_TOKEN'])

from models import *



# Send Mandril Template Message
def send_mandrill(template_name, message, template_content=[]):
    return mandrill_client.messages.send_template(template_name=template_name, message=message, template_content=template_content)

@celery.task
def do_task(task_id,type):

    if type == 'EmailTask':
        # Get TaskLog Instance and EmailConfiguration Instance
        task_log = TaskLog.query.filter_by(id=task_id).first()
        email_conf = task_log.email_configuration

        # Change the Task's status to IN_PROGRESS
        task_log.status = TaskLogStatus_Type.IN_PROGRESS
        db.session.commit()

        # Get All OutBoundEmails related to Task's email_configuration_id
        out_bounds = OutboundEmail.query.filter_by(email_configuration_id = task_log.email_configuration_id).all()

        for item in out_bounds:

            # Create Email Log to Pending Status
            email_log = EmailLog(Recipient = item.recipient, external_email_log_id = 0, status=EmailLogStatus_Type.PENDING)
            db.session.add(email_log)
            db.session.commit()

            # Send Mandrill Email
            message = {
                'from_email': 'noreply@elevationsoftware.io',
                'from_name': 'Elevation Software',
                'subject' : email_conf.subject,
                'to': [{'email': item.recipient.email_address,
                'name': '{} {}'.format(item.recipient.first_name, item.recipient.last_name)
                }],
            }
            try:
                result = send_mandrill(template_name=email_conf.email_template_id, message=message)

                email_log.external_email_log_id = result[0]['_id']

                # Change Email Log Status
                if result[0]['status'] == 'sent':
                    email_log.status = EmailLogStatus_Type.SENT
                elif result[0]['status'] == 'error':
                    # Create New TaskLogError
                    task_log_error = TaskLogError(error=result[0]['status']['code'],error_description=result[0]['status']['message'])
                    db.session.add(task_log_error)
                
            except mandrill.Error as e:
                # Mandrill errors are thrown as exceptions
                print('A mandrill error occurred: %s - %s' % (e.__class__, e))
                
                email_log.status = EmailLogStatus_Type.ERROR

                # Create New TaskLogError
                task_log_error = TaskLogError(error=0,error_description=str(e))
                db.session.add(task_log_error)
        
        # Completed_at
        email_conf.Completed_at = datetime.now()

    # TextMessage Task
    else:
        # Get TaskLog Instance and TextMessageConfiguration Instance
        task_log = TaskLog.query.filter_by(id=task_id).first()
        text_msg_conf = task_log.text_message_configuration

        # Change the Task's status to IN_PROGRESS
        task_log.status = TaskLogStatus_Type.IN_PROGRESS
        db.session.commit()

        # Get All OutBoundTextMessage related to Task's text_message_configuration_id
        out_bounds = OutboundTextMessage.query.filter_by(text_message_configuration_id = task_log.text_message_configuration_id).all()

        for item in out_bounds:
            # Create Text Message Log to Pending Status
            text_msg_log = TextMessageLog(Recipient = item.recipient, external_text_log_id = 0, status=EmailLogStatus_Type.PENDING)
            db.session.add(text_msg_log)
            db.session.commit()

            # Send Trilio Text Message
            try:
                result = twilio_client.messages \
                    .create(
                        body=text_msg_conf.message_body,
                        from_='+16789237694',
                        to=item.recipient.phone_number
                    )
                
                if result['status'] in ['sent','delivered','received']:
                    text_msg_log.status = EmailLogStatus_Type.SENT
                elif result['status'] in ['failed','undelivered']:
                    text_msg_log.status = EmailLogStatus_Type.ERROR
                
                if result['error_code']:
                    # Create New TaskLogError
                    task_log_error = TaskLogError(error=result['error_code'],error_description=result['error_message'])
                    db.session.add(task_log_error)

            except TwilioRestException as e:
                text_msg_log.status = EmailLogStatus_Type.ERROR
                print(e)
                # Create New TaskLogError
                task_log_error = TaskLogError(error=0,error_description=str(e))
                db.session.add(task_log_error)
            
            db.session.commit()
        
        # Completed_at
        text_msg_conf.Completed_at = datetime.now()
            
    # At the End, Change the Task's status to COMPLETED 
    task_log.status = TaskLogStatus_Type.COMPLETED
    db.session.commit()



# Create Task Function (Type : EmailTask or TextMessageTask)
def create_task(type,id):

    if type == 'EmailTask':
        result = EmailConfiguration.get_delete_put_post(id)
    else:
        result = TextMessageConfiguration.get_delete_put_post(id)

    if result.json['send_at'] != "":
        try:
            if type=='EmailTask':
                task_log = TaskLog(email_configuration_id = result.json['id'] , status=TaskLogStatus_Type.NOT_STARTED)
            else:
                task_log = TaskLog(text_message_configuration_id = result.json['id'] , status=TaskLogStatus_Type.NOT_STARTED)

            db.session.add(task_log)
            db.session.commit()

            # Scheduling ayncronous task in background with celery
            send_at = datetime.strptime(result.json['send_at'], '%Y-%m-%d %H:%M:%S')

            # Calcuate total seconds to do
            duration = send_at - datetime.now()
            duration = duration.total_seconds()

            if duration > 0.0:
                do_task.apply_async(args=[task_log.id,type], countdown=duration)

        except Exception as e:
            # Create New TaskLogError
            task_log_error = TaskLogError(error=0,error_description=str(e))
            db.session.add(task_log_error)
            db.session.commit()
    
    return result

# Email Configuration EndPoints
@app.route('/email_configurations/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/email_configurations',methods=['GET','POST'])
def email_configurations(id=None):

    # Customized for email_configuration POST API
    if request.method == 'POST':
        return create_task('EmailTask',id)

    # Default
    return EmailConfiguration.get_delete_put_post(id)

# Recipient EndPoints
@app.route('/recipients/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/recipients',methods=['GET','POST'])
def recipients(id=None):
    return Recipient.get_delete_put_post(id)

# EmailLog EndPoints
@app.route('/email_logs/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/email_logs',methods=['GET','POST'])
def email_logs(id=None):
    return EmailLog.get_delete_put_post(id)

# TaskLog EndPoints
@app.route('/task_logs/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/task_logs',methods=['GET','POST'])
def task_logs(id=None):
    return TaskLog.get_delete_put_post(id)

# TaskLogError EndPoints
@app.route('/task_errors/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/task_errors',methods=['GET','POST'])
def task_errors(id=None):
    return TaskLogError.get_delete_put_post(id)

# OutboundEmail EndPoints
@app.route('/outbound_emails/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/outbound_emails',methods=['GET','POST'])
def outbound_emails(id=None):

    # Get Post Data with CSV File

    # CSV Format
    # - row[0] : email
    # - row[1] : first name
    # - row[2] : last name
    # - row[3] : phone
    # - row[4] : email configuration id
    # - row[5] : text message configuration id

    if (id == None) and (request.method == 'POST'):
        if 'upload' in request.files:
            res = {'RecipientExists':[], 'CreatedOutboundEmails':[]}
            df = pd.read_csv(request.files.get('upload'))
            for i in range(len(df)):
                
                row = df.values[i]
                # Check Recipient Exists
                recipient = Recipient.query.filter_by(email_address = row[0], phone_number=row[3]).first()
                if recipient:
                    res['RecipientExists'].append({'email_address' : recipient.email_address, 'first_name' : recipient.first_name, 'last_name' : recipient.last_name, 'phone': recipient.phone_number})
                else:
                    recipient = Recipient(email_address = row[0] , first_name = row[1], last_name = row[2], phone_number=row[3])
                    db.session.add(recipient)
                    db.session.commit()
                
                # Check Email Configuration ID exists and Crate OutboundEmail
                if (EmailConfiguration.query.filter_by(id=row[4]).first()):
                    # Check Duplicated Rows in OutboundEmail
                    if OutboundEmail.query.filter_by(email_configuration_id = row[4]).filter_by(recipient = recipient).first() is None:
                        outbound = OutboundEmail(email_configuration_id = row[4], recipient = recipient)
                        db.session.add(outbound)
                        db.session.commit()
                        res['CreatedOutboundEmails'].append({'email_configuration_id':row[4], 'recipient_id' : recipient.id})

            return res, 201

    return OutboundEmail.get_delete_put_post(id)

# TextMessageConfiguration EndPoints
@app.route('/text_configurations/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/text_configurations',methods=['GET','POST'])
def text_message_configuration(id=None):

    # Customized for text_configurations POST API
    if request.method == 'POST':
        return create_task('TextMessageTask',id)

    # Default
    return TextMessageConfiguration.get_delete_put_post(id)

# OutboundTextMessage EndPoints
@app.route('/outbound_texts/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/outbound_texts',methods=['GET','POST'])
def outbound_text_message(id=None):

    # Get Post Data with CSV File

    # CSV Format
    # - row[0] : email
    # - row[1] : first name
    # - row[2] : last name
    # - row[3] : phone
    # - row[4] : email configuration id
    # - row[5] : text message configuration id

    if (id == None) and (request.method == 'POST'):
        if 'upload' in request.files:
            res = {'RecipientExists':[], 'CreatedOutboundTextMsgs':[]}
            df = pd.read_csv(request.files.get('upload'))
            for i in range(len(df)):
                
                row = df.values[i]
                # Check Recipient Exists
                recipient = Recipient.query.filter_by(email_address = row[0], phone_number=row[3]).first()
                if recipient:
                    res['RecipientExists'].append({'email_address' : recipient.email_address, 'first_name' : recipient.first_name, 'last_name' : recipient.last_name,'phone': recipient.phone_number})
                else:
                    recipient = Recipient(email_address = row[0] , first_name = row[1], last_name = row[2], phone_number=row[3])
                    db.session.add(recipient)
                    db.session.commit()
                
                # Check TextMessage Configuration ID exists and Crate OutboundTextMessage
                if (TextMessageConfiguration.query.filter_by(id=row[5]).first()):
                    # Check Duplicated Rows in OutboundTextMessage
                    if OutboundTextMessage.query.filter_by(text_message_configuration_id = row[5]).filter_by(recipient = recipient).first() is None:
                        outbound = OutboundTextMessage(text_message_configuration_id = row[5], recipient = recipient)
                        db.session.add(outbound)
                        db.session.commit()
                        res['CreatedOutboundTextMsgs'].append({'text_message_configuration_id':row[5], 'recipient_id' : recipient.id})

            return res, 201

    return OutboundTextMessage.get_delete_put_post(id)

# TextMessageLog EndPoints
@app.route('/text_msg_logs/<int:id>',methods=['GET','PUT','DELETE','POST'])
@app.route('/text_msg_logs',methods=['GET','POST'])
def text_message_log(id=None):
    return TextMessageLog.get_delete_put_post(id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
