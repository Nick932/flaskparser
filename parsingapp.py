from flask import Flask, jsonify, abort, make_response, send_file
from tools import ArchiveCreator, DataWriter, Scrapper,  Task_id
from tools import Status as status
from dbinterface import Database   
from celeryapp_settings import make_celery
    
    
    
parsapp = Flask(__name__)

parsapp.config.update(
    CELERY_BROKER_URL='pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)
celery = make_celery(parsapp)



db = Database('Scrappy')
db.create_table( table_name='scrapping_data', 
                 atr_names = ['id', 'uri', 'done'],
                 atr_types = ['int(6)', 'char(200)', 'char(10)'])



id_generator = Task_id()



@parsapp.route('/parsingapp/api/v1.0/tasks/', methods = ['GET'])
def get_tasks():
    
    
    tasks = db.select(table_name = 'scrapping_data')
    return jsonify( {'tasks': tasks} )



@parsapp.route('/parsingapp/api/v1.0/task/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    
    where_cl = 'id = %s' % task_id
    try:
        task_attrs = db.select(table_name = 'scrapping_data',
                               where_clause = where_cl)[0]
    except Exception:
        task_attrs = None
    
    url_to_download = 'some url to download' #WARNING: uncompleted

    if not task_attrs:
        abort(404)
    task_done = task_attrs[2]
    if task_done != 'False':
        return jsonify({'download url': url_to_download}), 200
    else:
        return jsonify({'task_done':task_done}), 200



@parsapp.route('/parsingapp/api/v1.0/new_task/<path:url_to_parse>', methods=['POST'])
def create_task(url_to_parse):


    if not url_to_parse:
        abort(400)
    id = id_generator.generate()
    db.insert('scrapping_data', id, url_to_parse, 'False')
    return jsonify({'task_id': id}), 201



@parsapp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@celery.task()
def scrappy(uri): #INFO: remake it
    x = Scrapper()
    a = x.collect_data(uri)
    return a


@parsapp.route('/parsingapp/api/v1.0/tasks/run/<path:url_to_parse>', methods=['GET'])
def run_task(url_to_parse):
    x = scrappy.delay(url_to_parse)
    a = x.get()
    return jsonify({'result':a}), 200


@parsapp.route('/parsingapp/api/v1.0/task/results/<int:task_id>')
def return_result(task_id):
    #filename = 'task_'+task_id
    name = task_id
    return send_file(name, as_attachment=True)


if __name__ == '__main__':

    # Run celery worker in a separate process automatically:
    '''loglevel = 'info'
    app = os.path.splitext(os.path.basename(__file__))[0]
    command = 'celery -A {0}.celery worker --loglevel={1}'.format(app, loglevel)
    Process(target = os.popen, args=(command, )).start()'''
    
    parsapp.run(debug=True)

