from tools import scrapper, DataWriter, ArchiveCreator
from celery_settings import celery
import os
from flask_app_settings import FILE_TYPE, FILE_DIR, ARCHIVE_DIR, ARCHIVE_TYPE

@celery.task
def scrapping(uri:str):
    '''
    Parses data from uri.
    Saves data to a file, then pack it to an archive.
    
    Takes 1 argument:
    uri (str) - a uri to parse.
    '''
    
    global FILE_DIR, FILE_TYPE, ARCHIVE_DIR, ARCHIVE_TYPE
    
    my_id = scrapping.request.id
    data = str(scrapper(uri))
    
    writer = DataWriter(file_folder = FILE_DIR, file_type = FILE_TYPE)
    writer.write(data, my_id)
    
    archivator = ArchiveCreator(archive_folder = ARCHIVE_DIR, archive_type = ARCHIVE_TYPE)
    file_path = os.path.join(os.getcwd(), FILE_DIR, my_id+'.'+FILE_TYPE)
    archivator.pack(file_path, my_id)
