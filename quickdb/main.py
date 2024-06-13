import os
import json
import pandas as pd
import logging


class Logger:
    """ Logger class to log the messages """
    def __init__(self, log_path):
        self.log_path = log_path
        self.logger = logging.getLogger(__name__)

        logging.basicConfig(filename=self.log_path, 
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='a')
        self.logger.info(f"Logger initialized with log path {self.log_path}")


class QuickDB(Logger):
    """  python database.py """
    def __init__(self, db_path="db.json", db_drop_path="quick_db_output", 
                 overwrite_db=False, debug=True, db_log_path="dedug.log"):
        super().__init__(db_log_path)
        """ Initialize the database """

        self.db_path = db_path
        self.debug = debug
        self.overwrite_db = overwrite_db
        self.db = self.__init_db()
        self.schema = self.db['schema']
        self.database = self.db['database']
        self.db_drop_path = db_drop_path
        self.db_log_path = db_log_path
           
    def __load_db_from_file(self):
        """ Load the database from the file """
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def __init_db(self):
        """" Initialize the database """

        if not self.overwrite_db and os.path.exists(self.db_path):
            self.logger.info(f"Loading database from {self.db_path}")
            return self.__load_db_from_file()
        
        if self.overwrite_db and os.path.exists(self.db_path):
            self.logger.info(f"Overwriting database from {self.db_path}")
            self.clear()
            return self.db

        self.logger.info(f"Creating new database at {self.db_path}")
        return {"database": {}, "schema": {}}

    def dump_db(self):
        """ Dump the database to the file """
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(self.db, f, indent=4)
                return True
        except json.JSONDecodeError:
            return False
        
    def dumb_table(self, table_name, output_format='json'):
        """ Dump the table to the file """
        if table_name not in self.db['database']:
            return False
        
        os.makedirs(self.db_drop_path, exist_ok=True)

        table_data = self.db['database'][table_name]

        if output_format == 'json':
            with open(os.path.join(self.db_drop_path, f"{table_name}.json"), 'w+') as f:
                json.dump(table_data, f, indent=4)
                self.logger.info(f"Table {table_name} dumped to {table_name}.json")
                return True

        if output_format == 'csv':
            df = pd.DataFrame(table_data).T
            df.to_csv(os.path.join(self.db_drop_path, f"{table_name}.csv"), index=False)
            self.logger.info(f"Table {table_name} dumped to {table_name}.csv")
            return True

        if output_format == 'excel':
            df = pd.DataFrame(table_data)
            df.to_excel(os.path.join(self.db_drop_path, f"{table_name}.xlsx"), index=False)
            self.logger.info(f"Table {table_name} dumped to {table_name}.xlsx")
            return True

        if output_format == 'df':
            return pd.DataFrame(table_data)

        if output_format == 'print':
            print(table_data)
            return True        
    
    def create_table(self, table_name, columns_list, primary_key=None):
        """ Create the schema of the database """

        if primary_key not in columns_list:
            raise ValueError(f"Primary key {primary_key} not in columns list")
        
        primary_key_index = columns_list.index(primary_key)
       
        self.schema[table_name] = {
            "columns_list": columns_list,
            "primary_key": primary_key,
            "primary_key_index": primary_key_index
        }

        self.db['schema'] = self.schema
        self.db['database'][table_name] = {}
        self.logger.info(f"Table {table_name} created with columns {columns_list} and primary key {primary_key}")
        self.dump_db()

    def get_table_names(self):
        """ Get all the tables in the database"""
        return list(self.schema.keys())
    
    def get_table(self, table_name):
        """ Get the table schema """
        return self.schema[table_name]
    
    def get_table_columns(self, table_name):
        """ Get the columns of the table """
        return self.schema[table_name]['columns_list']
    
    def get_table_primary_key(self, table_name):
        """ Get the primary key of the table """
        return self.schema[table_name]['primary_key']
    
    def insert_into(self, table_name, value, overwrite=False, dump_db=False):
        """ Set the key-value pair in the database """
        primary_value = value[self.schema[table_name]['primary_key_index']]
        columns_list = self.schema[table_name]['columns_list']

        if primary_value in self.db['database'][table_name] and not overwrite:
            return False
        
        if len(value) != len(columns_list):
            return False
        
        self.db["database"][table_name][primary_value] = dict(zip(columns_list, value))
        self.logger.info(f"Inserted {value} into {table_name}")

        if dump_db:
            self.dump_db()
        return True

    def get_db(self):
        """ Get the database along with the schema """
        return self.db

    def clear(self):
        """ Clear the database """
        self.db = {"database": {}, "schema": {}}
        self.dump_db()
        self.logger.info("Database cleared")
        return True
    
    def drop_table(self, table_name):
        """ Drop the table from the database """
        if table_name in self.db['database']:
            del self.db['database'][table_name]
            del self.db['schema'][table_name]
            self.dump_db()
            self.logger.info(f"Table {table_name} dropped")
            return True
        return False
    
    def delete(self, table_name, primary_value):
        """ Delete the key-value pair in the database """
        if primary_value in self.db['database'][table_name]:
            del self.db['database'][table_name][primary_value]
            self.dump_db()
            self.logger.info(f"Deleted {primary_value} from {table_name}")
            return True
        return False
    
    def update(self, table_name, primary_value, value):
        """ Update the key-value pair in the database """
        if primary_value in self.db['database'][table_name]:
            self.db['database'][table_name][primary_value] = value
            self.dump_db()
            self.logger.info(f"Updated {primary_value} in {table_name}")
            return True
        return False
    
    def search(self, table_name, primary_value):
        """ Search the key-value pair in the database """
        if primary_value in self.db['database'][table_name]:
            return self.db['database'][table_name][primary_value]
        return False
    
    def where(self, table_name, column_name, value):
        """ Search the key-value pair in the database """
        result = []
        for key, val in self.db['database'][table_name].items():
            if val[column_name] == value:
                result.append(val)
        return result
    
    def __repr__(self):
        return f"QuickDB(db_path={self.db_path}, db={self.db})"
    
    def __str__(self):
        return f"QuickDB(db_path={self.db_path}, db={self.db})"
    
    def __getitem__(self, key):
        return self.db["database"][key] if key in self.db["database"] else None
