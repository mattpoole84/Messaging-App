# App Secret Key
SECRET_KEY = '99633f69cf2dd0a127074c58c45b87fe9078449088fa9be54ccc3d2f6b72a485e524fad8da5435d432f13bae4b7759ce7e186160d028902e64ec2ae7226293e180'

# Mandrill Client Key
MANDRILL_KEY = ''

# Database Configuration
USERNAME = 'root'
PASSWORD = 'root'
NAME = 'email_task_app'
DATABASE = 'mysql://{}:{}@db/{}'.format(USERNAME,PASSWORD,NAME)

# Celery Configuration
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

# Twilio Key
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''