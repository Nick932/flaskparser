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
    '''
    Implements interface to an archivation process.
    Takes 2 optional arguments:
    archive_type (str) - an archive type. Default 'zip'.
    archive_folder(str) - a name of the folder for archives in current working dir. .
    '''
    
    def __init__(self, archive_type = 'zip', archive_folder = 'archives'):
        
        self.archive_folder = archive_folder
        cwd = os.getcwd()+os.sep
        try:
            os.mkdir(cwd+archive_folder)
        except FileExistsError:
            pass
        self.path_to_archive = cwd+archive_folder+os.sep
        self.archive_type = archive_type
        
        
    def pack(self, full_file_path:str, archive_name:str):
        '''
        Packs the given file into an archive.
        
        Takes 2 arguments:
        full_file_path (str) - a full path to the file, including a full file name.
        archive_name (str) - a name of the archive file.
        '''
        cwd = os.getcwd()
        path_to_file = os.path.split(full_file_path)[0]
        file_name = os.path.split(full_file_path)[1]
        archive_file = archive_name+'.'+self.archive_type
        #TODO: LOGGING! print(os.getcwd())
        os.chdir(self.archive_folder) # We create the archive in necessary folder...
        data_archive = zipfile.ZipFile(archive_file, 'w')
        #TODO: LOGGING! print(os.getcwd())
        os.chdir(path_to_file) # ... then we go to the file's folder, to pack the
        # file to the archive:
        #TODO: LOGGING! print(os.getcwd())
        #TODO: LOGGING! print(file_name)
        data_archive.write(file_name, compress_type = zipfile.ZIP_DEFLATED)
        data_archive.close()
        #TODO: LOGGING! print(os.getcwd())
        os.chdir(cwd) # Now let's go back to the original directory. 
        #TODO: LOGGING! print(os.getcwd())


def scrapper(uri:str):
    '''
    Collects data from a given uri.
    
    Expecting 1 argument:
    uri (str) - uri to scrapp.
    
    Returns the result of scrapping.
    '''
    page_response = requests.get(uri, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    data = page_content.find_all()
    return data



class DataWriter:
    '''
    A special interface for writing scrapper's results.
    
    Takes 2 optional arguments:
    
    file_folder (str) - a folder name for files with scrapping data, located
                        in current working directory. 'files' by default.
    file_type (str) - a necessary type of file. 'txt' by default.
    '''
    
    def __init__(self, file_folder = 'files', file_type = 'txt'):
        
        cwd = os.getcwd()+os.sep
        try:
            os.mkdir(cwd+file_folder)
        except FileExistsError:
            pass
        self.path = cwd+file_folder+os.sep
        self.filetype = file_type


    def write(self, data:str, filename:str):
        '''
        Writes the data to the file.
        
        Takes 2 arguments:
        data (str) - the necessary data to write down.
        
        '''
        datafile = self.path+filename+'.'+self.filetype
        file = open(datafile, 'w')
        file.write(data)
        file.close()
