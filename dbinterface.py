'''
Implements a database interface with the Database class.
'''

import sqlite3



def connect_to(dbname):
    
    def wrapper(func):
        def onCall(*args, **kwargs):
            connection = sqlite3.connect(dbname)
            cursor = connection.cursor()
            command = func(*args, **kwargs)
            cursor.execute(command)
            connection.commit()
            connection.close()
        return onCall
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
        
    
    def create_table(self, table_name:str, atr_names:list, atr_types:list):
        
        connection, cursor = self.connect(self.database_name)
        
        columns_list = list(zip(atr_names, atr_types))
        table_command = 'create table {0}('.format(table_name)
        
        for column in columns_list:
            column = str(column[0])+' '+str(column[1])+', '
            table_command+=column
        table_command = self._command_format(table_command)
        try:
            cursor.execute(table_command)
            connection.commit()
        except sqlite3.OperationalError as exception:
            print('Exception!', exception) #TODO: LOGGING!
            pass
            
            
    def insert(self, table_name:str, *values):
        
        connection, cursor = self.connect(self.database_name)
        values_tuple = tuple(values)
        valcount = '?,'*len(values_tuple)
        insert_command = "insert into {0} values({1})".format(table_name, valcount)
        insert_command = self._command_format(insert_command)
        cursor.execute(insert_command, values_tuple)
        connection.commit()
        
        
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
        return results
        
        
    def update(self, table_name:str, atribute:str, value,  where_clause:str):
        
        value = '"{0}"'.format(value) #NOTE: what if value is integer?
        connection, cursor = self.connect(self.database_name)
        update_command = 'update {0} set {1}={2} where {3}'.format(table_name, 
                            atribute, value, where_clause)
        print(update_command)
        cursor.execute(update_command)
        connection.commit()
    
