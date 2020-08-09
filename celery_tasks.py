from dbtable import scrappy_database as db
from tools import Scrapper, DataWriter, ArchiveCreator
from celery_settings import celery
import os

@celery.task
def scrapping(uri):
    '''
    Меняет статус задачи в БД на 'in process'.
    
    Собирает данные из uri.
    Сохраняет данные в файл, а затем упаковывает его в архив.
    
    Меняет статус задачи в БД.    
    '''
    
    my_id = scrapping.request.id
    db.insert('scrapping_data', my_id, uri, 'In progress')
    
    scrappy = Scrapper()
    data = scrappy.collect_data(uri)
    
    path = os.getcwd()+os.sep
    writer = DataWriter(path=path)
    filename = 'task_data_'+my_id
    print('#'*8)
    print(data)
    print(data.__class__)
    writer.write(data, filename)
    
    archivator = ArchiveCreator()
    archivator.pack(filename+writer.filetype, filename)
    
    where_clause = 'id={0}'.format(my_id)
    db.update('scrapping_data', 'status', 'Done', where_clause)
