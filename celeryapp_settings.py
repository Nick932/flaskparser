from celery import Celery
#import os

def make_celery(app, loglevel = 'info'):

    celery = Celery(
        app.import_name, 
        #os.path.splitext(os.path.basename(__file__))[0],
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    
    return celery
