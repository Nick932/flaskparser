from dbtable import scrappy_database as db
from tools import Scrapper, DataWriter, ArchiveCreator, status
from celery_settings import celery
import os



ARCHIVE_TYPE = 'zip'



@celery.task
def scrapping(uri):
    '''
    Меняет статус задачи в БД на 'in process'.
    
    Собирает данные из uri.
    Сохраняет данные в файл, а затем упаковывает его в архив.
    
    Меняет статус задачи в БД.    
    '''
    
    my_id = scrapping.request.id
    db.insert('scrapping_data', my_id, uri, status.in_progress.value)
    
    scrappy = Scrapper()
    data = str(scrappy.collect_data(uri))
    
    path = os.getcwd()+os.sep
    
    writer = DataWriter(path=path)
    filename = 'task_data_'+my_id
    writer.write(data, filename)
    
    global ARCHIVE_TYPE
    archivator = ArchiveCreator(archive_type = ARCHIVE_TYPE)
    archivator.pack(filename+writer.filetype, filename)
    
    where_clause = 'id="{0}"'.format(my_id) #NOTE: client mustn't know that quotes should be used?
    db.update('scrapping_data', 'status', status.done.value, where_clause)
