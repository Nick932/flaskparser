from dbtables import scrappy_database as db
from tools import Scrapper, DataWriter, ArchiveCreator, status
from celery_settings import celery
import os


@celery.task
def scrapping(uri:str, archive_type:str, archive_folder:str, file_type:str, file_folder:str ):
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
    
    writer = DataWriter(file_folder = file_folder, file_type = file_type)
    writer.write(data, my_id)
    
    archivator = ArchiveCreator(archive_folder = archive_folder, archive_type = archive_type)
    archivator.pack(os.getcwd()+os.sep+file_folder+os.sep+my_id+'.'+file_type, my_id)
    
    where_clause = 'id="{0}"'.format(my_id) #NOTE: client mustn't know that quotes should be used?
    db.update('scrapping_data', 'status', status.done.value, where_clause)
