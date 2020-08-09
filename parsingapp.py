from flask import Flask, jsonify, abort, make_response, send_file,  url_for
from tools import Task_id
from tools import Status as status
from dbtable import scrappy_database as db
import celery_settings
from celery_tasks import scrapping
from flask_app_settings import parsapp

celery = celery_settings.celery



@parsapp.route('/parsingapp/api/v1.0/tasks/', methods = ['GET'])
def get_tasks():
    
    
    tasks = db.select(table_name = 'scrapping_data')
    return jsonify( {'tasks': tasks} )



@parsapp.route('/parsingapp/api/v1.0/task/<string:task_id>', methods = ['GET'])
def get_task(task_id):
    '''
    Получает id.
    
    Проверяет, завершена ли задача из БД с таким id.
    Если завершена, 
        возвращает ссылку на скачивание 
        архива с задачей.
    Если нет, 
        возвращает статус задачи.
    '''
    
    where_cl = 'id = %s' % task_id
    
    try:
        task_attrs = db.select(table_name = 'scrapping_data',
                               where_clause = where_cl
                               )[0]
                               
    #NOTE: remake this fragment:
    except Exception:
        task_attrs = None
    if not task_attrs:
        abort(404)
        
    task_status = task_attrs[2]
    if task_status == 'Done':
        name = 'task_data_{0}'.format(task_id)
        url = url_for('download', filename = name)
        return jsonify({'url_to_download': url})
    else:
        return jsonify({'task_status':task_status}), 200



@parsapp.route('/parsingapp/api/v1.0/new_task/<path:url_to_parse>', methods=['POST'])
def create_task(url_to_parse):
    '''
    Создаёт асинхронную задачу в Celery.
    Возвращает id задачи, заданный в БД.
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
    name = filename
    return send_file(name, as_attachment=True)


if __name__ == '__main__':

    # Run celery worker in a separate process automatically:
    '''loglevel = 'info'
    app = os.path.splitext(os.path.basename(__file__))[0]
    command = 'celery -A {0}.celery worker --loglevel={1}'.format(app, loglevel)
    Process(target = os.popen, args=(command, )).start()'''
    
    parsapp.run(debug=True)

