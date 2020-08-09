'''
Implements a database interface with the Database class.
'''

import sqlite3
from functools import wraps


def connect_to_database(method):
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        
        dbname = self.database_name
        print('Connection opened.')
        connection = sqlite3.connect(dbname)
        cursor = connection.cursor()
        command = method(self, *args, **kwargs)
        print('Command to the database:\n', command)
        
        try:
            cursor.execute(command)
            connection.commit()
        except sqlite3.OperationalError as exception:
            print('Exception!', exception) #TODO: LOGGING!
            pass
        else:
            print('Command executed successfully.')
        connection.close()
        print('Connection closed.')

    return wrapper


class Database:
    '''
    Interface to a database.
    Takes 1 initial argument: database name.
    '''
    
    def __init__(self, dbname:str):
        self.database_name = 'Db_{0}'.format(dbname)
        
    def _command_format(self, command:str):
        '''
        Used to avoid syntax errors in database's commands.
        
        Takes 1 argument: database command.
        Truncates 2 last symbols of command and adds ')' to it.
        
        Returns formatted command.
        '''
        
        fcom=command[:-2]+')'
        return fcom
    
    
    def connect(self, dbname):
        connection = sqlite3.connect(dbname)
        cursor = connection.cursor()
        return connection, cursor
        
    @connect_to_database
    def create_table(self, table_name:str, atr_names:list, atr_types:list):
        
        columns_list = list(zip(atr_names, atr_types))
        table_command = 'create table {0}('.format(table_name)
        
        for column in columns_list:
            column = str(column[0])+' '+str(column[1])+', '
            table_command+=column
        table_command = self._command_format(table_command)
        return table_command

    @connect_to_database
    def insert(self, table_name:str, *values):
        
        values_tuple = tuple(values)
        insert_command = "insert into {0} values {1}".format(table_name, values_tuple)
        return insert_command
        
        
        
    def select(self, table_name:str, atributes='*', where_clause=None):
        
        connection, cursor = self.connect(self.database_name)
        if where_clause:
            select_command = 'select {0} from {1} where {2}'.format(atributes, 
                            table_name, where_clause)
        else:
            select_command = 'select {0} from {1}'.format(atributes, 
                            table_name)
                            
        cursor.execute(select_command)
        results = cursor.fetchall()
        connection.close()
        return results
        
        
        
    @connect_to_database
    def update(self, table_name:str, atribute:str, value,  where_clause:str):
        
        value = '"{0}"'.format(value) #NOTE: what if value is integer?
        connection, cursor = self.connect(self.database_name)
        update_command = 'update {0} set {1}={2} where {3}'.format(table_name, 
                            atribute, value, where_clause)
        return update_command
    
