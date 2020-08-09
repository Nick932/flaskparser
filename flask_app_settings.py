from flask import Flask



parsapp = Flask(__name__)

parsapp.config.update(
    CELERY_BROKER_URL='pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)
