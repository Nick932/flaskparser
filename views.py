from flask import jsonify, abort, make_response, send_file,  url_for
import celery_settings
from celery_tasks import scrapping
from flask_app_settings import parsapp, ARCHIVE_DIR, ARCHIVE_TYPE
import os



celery = celery_settings.celery



@parsapp.route('/parsingapp/api/v1.0/task/<string:task_id>', methods = ['GET'])
def get_task(task_id):
    '''
    Checks if the task done or not.
    
    If done: returns uri to download archive with the task's results.
    If not: returns the task's status.
    '''

    if scrapping.AsyncResult(task_id).ready():
        url = url_for('download', filename = task_id, _external = True)
        return jsonify({'url_to_download': url})
    else:
        return jsonify({'task_status':'In progress'})



@parsapp.route('/parsingapp/api/v1.0/new_task/<path:url_to_parse>', methods=['POST'])
def create_task(url_to_parse):
    '''
    Creates an asynchronous Celery task.
    Returns id of the task.
    '''
    
    if not url_to_parse:
        abort(400)
    
    task = scrapping.apply_async(args=(url_to_parse,))
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
    return send_file(ARCHIVE_DIR+os.sep+filename+'.'+ARCHIVE_TYPE, as_attachment=True)
