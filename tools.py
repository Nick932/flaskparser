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
    
    
    def __init__(self, archive_type = 'zip'):
        
        self.path_to_cwd = os.getcwd()+os.sep
        self.archive_type = archive_type
        
        
    def pack(self, file_to_archive:str, archive_name:str):
        
        data_file_name = file_to_archive
        archive_file = archive_name+'.'+self.archive_type
        data_archive = zipfile.ZipFile(archive_file, 'w')
        data_archive.write(data_file_name, compress_type = zipfile.ZIP_DEFLATED)
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
    
    
    def __init__(self, path, filetype = '.txt'):
        self.path = path
        self.filetype = filetype


    def write(self, data:str, filename:str):
        
        datafile = self.path+os.sep+filename+self.filetype
        file = open(datafile, 'w')
        file.write(data)
        file.close()
