import sqlite3

class Database:
    
    
    def __init__(self, dbname):
        self.database_name = 'Db_{0}'.format(dbname)
        
        
    def command_format(self, command:str):
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
        table_command = self.command_format(table_command)
        try:
            cursor.execute(table_command)
            connection.commit()
        except sqlite3.OperationalError as exception:
            print('Exception!', exception) #WARNING: fix me
            pass
            
            
    def insert(self, table_name:str, *values):
        
        connection, cursor = self.connect(self.database_name)
        values_tuple = tuple(values)
        valcount = '?,'*len(values_tuple)
        insert_command = "insert into {0} values({1})".format(table_name, valcount)
        insert_command = self.command_format(insert_command)
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
        
        
    def update(self, table_name:str, atribute:str, value:str,  where_clause:str):
        
        connection, cursor = self.connect(self.database_name)
        update_command = 'update {0} set {1}={2} where {3}'.format(table_name, 
                            atribute, value, where_clause)
        cursor.execute(update_command)
        connection.commit()
    
