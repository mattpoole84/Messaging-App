# Messaging App

## Tecnical Stacks
* Python 3
* Flask-API
* Mandrill (https://mandrillapp.com/api/docs/)
* Twilio (https://www.twilio.com/docs/libraries/python)
* Celery for Task Scheduler
* Redis for Message Broker

## Installation
* Install Python 3.7

* Install Required Modules:
```bash
pip install -r requirements.txt
```
* Install MySQL Database and Create New Database
    You can check config.py file for Database configuration( default: email_task_app , username:root, password:'' )
    Also there are Mandrill Client Key and Celery/Redis Configuration.

* Install Redis And Start Server
    
* Create Database Tables and Start Flask Server
```bash
	python create_tables.py
	python app.py
```
* Start Celery Worker
```bash
	celery -A app.celery worker -l INFO
```

## Important Information
1. Celery+4.0 not supported in windows system, It causes some warning or errors. So prefer other unix or linux system for server.
2. Almost Models (GET, PUT, POST ,DELETE) API endpoints are available.
3. When upload csv file with multi-part, requested csv file should be stored in 'upload' parameter. (request.files['upload'])
4. Also refer the test/upload.csv file format for csv uploading.
