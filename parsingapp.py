from flask import Flask, jsonify, abort, make_response
from scrapper import scrapper
from dbinterface import Database
import threading, time


parsapp = Flask(__name__)

db = Database('Scrappy')
db.create_table(table_name='scrapping_data', atr_names = ['id', 'uri', 'done'],
            atr_types = ['int(6)', 'char(200)', 'char(10)'])


class Task_id:
    def __init__(self):
        self.id = 0
    def generate(self):
        task_id = self.id
        self.id+=1
        return task_id

id_generator = Task_id()



@parsapp.route('/parsingapp/api/v1.0/tasks/', methods = ['GET'])
def get_tasks():
    
    tasks = db.select(table_name = 'scrapping_data')
    return jsonify( {'tasks': tasks} )


@parsapp.route('/parsingapp/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    
    where_cl = 'id = %s' % task_id
    
    try:
        task_attrs = db.select(table_name = 'scrapping_data',
                    where_clause = where_cl)[0]
    except Exception:
        task_attrs = None
    
    url_to_download = 'some url to download'

    if not task_attrs:
        abort(404)
    
    task_done = task_attrs[2]
    if task_done != 'False':
        return jsonify({'download url': url_to_download}), 200
    else:
        return jsonify({'task_done':task_done}), 200


@parsapp.route('/parsingapp/api/v1.0/tasks/<path:url_to_parse>', methods=['POST'])
def create_task(url_to_parse):

    if not url_to_parse:
        abort(400)


    id = id_generator.generate()
    db.insert('scrapping_data', id, url_to_parse, 'False')

    return jsonify({'task_id': id}), 201


@parsapp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    parsapp.run(debug=True)
