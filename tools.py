import zipfile
import os
from bs4 import BeautifulSoup
import requests
import enum



@enum.unique
class Status(enum.Enum):
    done = 'Done'
    in_progress = 'In progress'

status = Status



class ArchiveCreator:
    
    
    def __init__(self, archive_type = 'zip', archive_folder = 'archives'):
        
        cwd = os.getcwd()+os.sep
        try:
            os.mkdir(cwd+archive_folder)
        except FileExistsError:
            pass
        self.path_to_archive = cwd+archive_folder+os.sep
        self.archive_type = archive_type
        
        
    def pack(self, file_to_archive:str, archive_name:str):
        #FIXME: problem with archive content.
        archive_file = archive_name+'.'+self.archive_type
        data_archive = zipfile.ZipFile(archive_file, 'w')
        data_archive.write(file_to_archive, compress_type = zipfile.ZIP_DEFLATED)
        data_archive.close()



class Scrapper:


    def __init__(self):
        
        self.data = None


    def collect_data(self, uri:str):
        
        page_response = requests.get(uri, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        self.data = page_content.find_all()
        return self.data



class DataWriter:
    
    
    def __init__(self, file_folder = 'files', file_type = '.txt'):
        
        cwd = os.getcwd()+os.sep
        try:
            os.mkdir(cwd+file_folder)
        except FileExistsError:
            pass
        self.path = cwd+file_folder+os.sep
        self.filetype = file_type


    def write(self, data:str, filename:str):
        
        datafile = self.path+filename+'.'+self.filetype
        file = open(datafile, 'w')
        file.write(data)
        file.close()
