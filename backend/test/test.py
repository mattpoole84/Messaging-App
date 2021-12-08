# test.py for pytest
from app import app, send_mandrill,twilio_client
from flask import json
import pytest
from models import *
import mandrill
from twilio.base.exceptions import TwilioRestException


#- Add Email Configuration
#- Delete Task Log ( Not Started Status) 
#- Delete Email Configuration that just added

def test_email_configuration_api():

    # Add Email Configuration
    response = app.test_client().post(
        '/email_configurations',
        data=json.dumps(
            {
                "email_template_id": "1",
                "send_at": "2020-10-16 19:20:20",
                "subject": "test"
            }
        ),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['send_at'] == "2020-10-16 19:20:20"

    # Delete Task Log ( Not Started Status) 
    task_log = TaskLog.query.filter_by(email_configuration_id=data['id']).delete()
    db.session.commit()

    # Delete Email Configurator that just added 
    response = app.test_client().delete('/email_configurations/{}'.format(data['id']))
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['message'] == "Deleted"

def test_text_msg_configuration_api():

    # Add TextMessage Configuration
    response = app.test_client().post(
        '/text_configurations',
        data=json.dumps(
            {
                "message_body": "test",
                "send_at": "2020-10-16 19:20:20",
            }
        ),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['send_at'] == "2020-10-16 19:20:20"

    # Delete Task Log ( Not Started Status) 
    task_log = TaskLog.query.filter_by(text_message_configuration_id=data['id']).delete()
    db.session.commit()

    # Delete Email Configurator that just added 
    response = app.test_client().delete('/text_configurations/{}'.format(data['id']))
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['message'] == "Deleted"

#Test OutBoundEmail and OutBoundTextMessage API with uploading csv file.
def test_uploading_csv():
    """Test can upload csv."""

    data={}

    data['upload'] = (open("upload.csv", "rb"),'upload.csv')

    # OutBoundEmail
    response = app.test_client().post('/outbound_emails', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    
    data = json.loads(response.get_data(as_text=True))

    print("\n######### Outbound Email Response #############")
    print(data)

    assert response.status_code == 201

    data={}

    data['upload'] = (open("upload.csv", "rb"),'upload.csv')
    # OutBoundTextMessage
    response = app.test_client().post('/outbound_texts', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    
    data = json.loads(response.get_data(as_text=True))

    print("\n######### Outbound TextMessage Response #############")
    print(data)

    assert response.status_code == 201

# Test Mandrill Integration
def test_Mandrill():
    message = {
            'from_email': 'noreply@elevationsoftware.io',
            'from_name': 'Elevation Software',
            'subject' : "test",
            'to': [{'email': "test@test.com",
                'name': '{} {}'.format("test", "test")
            }],
        }
    try:
        result = send_mandrill(template_name="xxx", message=message)
    except mandrill.Error as e:
        assert str(e) == 'No such template "xxx"'

# Test Twilio Integration
def test_Twilio():

    print('\n######### Twilio Test Response #############')
    # Send Trilio Text Message
    try:
        result = twilio_client.messages \
            .create(
                    body='test',
                    from_='+16789237694',
                    to='xxxx'
            )
    except TwilioRestException as e:
        print(e)