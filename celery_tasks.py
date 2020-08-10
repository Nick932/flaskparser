from dbtables import scrappy_database as db
from tools import scrapper, DataWriter, ArchiveCreator, status
from celery_settings import celery
import os
from flask_app_settings import FILE_TYPE, FILE_DIR, ARCHIVE_DIR, ARCHIVE_TYPE

@celery.task
def scrapping(uri:str):
    '''
    Changes the task's status in the database to 'in process'.
    
    Parses data from uri.
    Saves data to a file, then pack it to an archive.
    
    Changes the task's status to 'Done'.    
    
    Takes 1 argument:
    uri (str) - a uri to parse.
    '''
    
    global FILE_DIR, FILE_TYPE, ARCHIVE_DIR, ARCHIVE_TYPE
    
    my_id = scrapping.request.id
    db.insert('scrapping_data', my_id, uri, status.in_progress.value)
    data = str(scrapper(uri))
    
    writer = DataWriter(file_folder = FILE_DIR, file_type = FILE_TYPE)
    writer.write(data, my_id)
    
    archivator = ArchiveCreator(archive_folder = ARCHIVE_DIR, archive_type = ARCHIVE_TYPE)
    file_path = os.path.join(os.getcwd(), FILE_DIR, my_id+'.'+FILE_TYPE)
    archivator.pack(file_path, my_id)
    
    where_clause = 'id="{0}"'.format(my_id) #NOTE: client mustn't know that quotes should be used?
    db.update('scrapping_data', 'status', status.done.value, where_clause)
