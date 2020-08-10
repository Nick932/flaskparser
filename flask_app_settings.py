from flask import Flask


FILE_TYPE = 'txt'
FILE_DIR = 'files1'
ARCHIVE_DIR = 'archives1'
ARCHIVE_TYPE = 'zip'


parsapp = Flask(__name__)

parsapp.config.update(
    CELERY_BROKER_URL='pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND='db+postgresql://parserator:wannaparse@localhost/parsingdatabase'
)

import views
