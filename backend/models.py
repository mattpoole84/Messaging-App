from app import db
import enum
from flask_serialize import FlaskSerializeMixin

FlaskSerializeMixin.db = db

# Email Configuration Model
class EmailConfiguration(db.Model ,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email_template_id = db.Column(db.String(100))
    subject = db.Column(db.String(255))
    send_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    create_fields = update_fields = ['email_template_id', 'subject', 'send_at']

# Recipient Model
class Recipient(db.Model ,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email_address = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))

    create_fields = update_fields = ['email_address', 'first_name', 'last_name' ,'phone_number']

# OutboundEmail Model
class OutboundEmail(db.Model ,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    recipient = db.relationship('Recipient')
    email_configuration_id = db.Column(db.Integer, db.ForeignKey('email_configuration.id'))
    email_configuration = db.relationship('EmailConfiguration')

    create_fields = update_fields = ['recipient_id', 'email_configuration_id']

# EmailLog Model
class EmailLogStatus_Type(enum.Enum):
    SENT = "Sent"
    ERROR = "Error"
    PENDING = "Pending"

class EmailLog(db.Model ,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    recipient = db.relationship('Recipient')
    external_email_log_id = db.Column(db.Integer)
    status = db.Column(db.Enum(EmailLogStatus_Type))

    create_fields = update_fields = ['recipient_id', 'external_email_log_id', 'status']

# TaskLog Model
class TaskLogStatus_Type(enum.Enum):
    COMPLETED = "Completed"
    IN_PROGRESS = "In_Progress"
    NOT_STARTED = "Not_Started"

class TaskLog(db.Model ,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email_configuration_id = db.Column(db.Integer, db.ForeignKey('email_configuration.id'))
    email_configuration = db.relationship('EmailConfiguration')
    text_message_configuration_id = db.Column(db.Integer, db.ForeignKey('text_message_configuration.id'))
    text_message_configuration = db.relationship('TextMessageConfiguration')
    status = db.Column(db.Enum(TaskLogStatus_Type))

    create_fields = update_fields = ['email_configuration_id', 'text_message_configuration_id' , 'status']

# TaskLogError Model
class TaskLogError(db.Model ,FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    error = db.Column(db.Integer)
    error_description = db.Column(db.String(255))

    create_fields = update_fields = ['error', 'error_description']

# TextMessageConfiguration Model
class TextMessageConfiguration(db.Model, FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    message_body = db.Column(db.Text)
    send_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    create_fields = update_fields = ['message_body', 'send_at']

# OutboundTextMessage Model
class OutboundTextMessage(db.Model, FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    recipient = db.relationship('Recipient')
    text_message_configuration_id = db.Column(db.Integer, db.ForeignKey('text_message_configuration.id'))
    text_message_configuration = db.relationship('TextMessageConfiguration')

    create_fields = update_fields = ['recipient_id', 'text_message_configuration_id']

# TextMessageLog Model
class TextMessageLog(db.Model, FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    recipient = db.relationship('Recipient')
    external_text_log_id = db.Column(db.Integer)
    status = db.Column(db.Enum(EmailLogStatus_Type))

    create_fields = update_fields = ['recipient_id', 'external_text_log_id', 'status']