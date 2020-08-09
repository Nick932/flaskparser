from flask import jsonify, abort, make_response, send_file,  url_for
from tools import status
from dbtable import scrappy_database as db
import celery_settings
from celery_tasks import scrapping, ARCHIVE_TYPE
from flask_app_settings import parsapp
import sys

celery = celery_settings.celery



@parsapp.route('/parsingapp/api/v1.0/tasks/', methods = ['GET'])
def get_tasks():
    '''
    Returns all available tasks.
    '''
    
    tasks = db.select(table_name = 'scrapping_data')
    return jsonify( {'tasks': tasks} ), 200



@parsapp.route('/parsingapp/api/v1.0/task/<string:task_id>', methods = ['GET'])
def get_task(task_id):
    '''
    Returns task with designated id.
    
    Checks if the task done or not.
    If done: returns uri to download archive with the task's results.
    If not: returns the task's status.
    '''
    
    where_cl = 'id = "%s"' % task_id #NOTE: client mustn't know that quotes should be used?
    
    try:
        task_attrs = db.select(table_name = 'scrapping_data',
                               where_clause = where_cl
                               )[0]
    except Exception:
        print(sys.exc_info()) #TODO: LOGGING!
        task_attrs = None

    if not task_attrs:
        abort(404)
        
    task_status = task_attrs[2]
    if task_status == status.done.value:
        name = 'task_data_{0}'.format(task_id)
        url = url_for('download', filename = name, _external = True)
        return jsonify({'url_to_download': url}), 200
    else:
        return jsonify({'task_status':task_status}), 200



@parsapp.route('/parsingapp/api/v1.0/new_task/<path:url_to_parse>', methods=['POST'])
def create_task(url_to_parse):
    '''
    Creates an asynchronous Celery task.
    Returns id of the task.
    '''
    
    if not url_to_parse:
        abort(400)
    
    task = scrapping.apply_async(args=(url_to_parse, ))
    id = task.id
    return jsonify({'task_id': id}), 201



@parsapp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@parsapp.route('/parsingapp/api/v1.0/task/download/<string:filename>')
def download(filename):
    '''
    Sends the designated file.
    '''
    return send_file(filename+'.'+ARCHIVE_TYPE, as_attachment=True)


if __name__ == '__main__':

    '''
    # You can also automatically run celery worker in a separate process:
    loglevel = 'info'
    app = os.path.splitext(os.path.basename(__file__))[0]
    command = 'celery -A {0}.celery worker --loglevel={1}'.format(app, loglevel)
    Process(target = os.popen, args=(command, )).start()
    '''
    
    parsapp.run(debug=True)

