from flask_app_settings import parsapp

if __name__ == '__main__':

    '''
    # You can also automatically run celery worker in a separate process:
    loglevel = 'info'
    app = os.path.splitext(os.path.basename(__file__))[0]
    command = 'celery -A {0}.celery worker --loglevel={1}'.format(app, loglevel)
    Process(target = os.popen, args=(command, )).start()
    '''
    
    parsapp.run(debug=True)
