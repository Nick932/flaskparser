from dbinterface import Database

scrappy_database = Database('Scrappy')
scrappy_database.create_table( table_name='scrapping_data', 
                 atr_names = ['id', 'uri', 'status'],
                 atr_types = ['char(100)', 'char(200)', 'char(11)'])
