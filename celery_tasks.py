from dbtables import scrappy_database as db
from tools import Scrapper, DataWriter, ArchiveCreator, status
from celery_settings import celery
import os


@celery.task
def scrapping(uri:str, archive_type:str, archive_folder:str, file_type:str, file_folder:str ):
    '''
    Changes the task's status in the database to 'in process'.
    
    Parses data from uri.
    Saves data to a file, then pack it to an archive.
    
    Changes the task's status to 'Done'.    
    
    Takes 5 arguments:
    
    uri (str) - a uri to parse.
    archive_type (str) - a type of archive file.
    archive_folder (str) - a folder name for archive in the current working directory.
    file_type (str) - a type of file with the parsing data.
    file_folder (str) - a folder name for files in the current working directory.
    '''
    
    my_id = scrapping.request.id
    db.insert('scrapping_data', my_id, uri, status.in_progress.value)
    scrappy = Scrapper()
    data = str(scrappy.collect_data(uri))
    
    writer = DataWriter(file_folder = file_folder, file_type = file_type)
    writer.write(data, my_id)
    
    archivator = ArchiveCreator(archive_folder = archive_folder, archive_type = archive_type)
    file_path = os.path.join(os.getcwd(), file_folder, my_id+'.'+file_type)
    archivator.pack(file_path, my_id)
    
    where_clause = 'id="{0}"'.format(my_id) #NOTE: client mustn't know that quotes should be used?
    db.update('scrapping_data', 'status', status.done.value, where_clause)
