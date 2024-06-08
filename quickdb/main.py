import os
import json


class QuickDB:
    """  python database.py """
    def __init__(self, db_path="db.json", overwrite_db=False, debug=True):
        self.db_path = db_path
        self.debug = debug
        self.overwrite_db = overwrite_db
        self.db = self.__init_db()
        self.primary_key = None
        self.primary_value_index = None
        self.primary_value = None

    def __load_db_from_file(self):
        """ Load the database from the file """
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def __init_db(self):
        """" Initialize the database """

        if not self.overwrite_db and os.path.exists(self.db_path):
            return self.__load_db_from_file()
        
        if self.overwrite_db and os.path.exists(self.db_path):
            self.clear()
            return self.db

        return {}

    def dump_db(self):
        """ Dump the database to the file """
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(self.db, f, indent=4)
                return True
        except json.JSONDecodeError:
            return False
    
    def create_table(self, columns_list, primary_key=None):
        """ Create the schema of the database """
        self.primary_key = primary_key
        self.columns_list = columns_list
        if primary_key not in columns_list:
            raise ValueError(f"Primary key {primary_key} not in columns list")
        self.primary_value_index = self.columns_list.index(self.primary_key)

        self.schema = {
            "columns_list": self.columns_list,
            "primary_key": self.primary_key,
            "primary_value_index": self.primary_value_index
        }

        self.db['schema'] = self.schema
        self.dump_db()

    def get_table(self):
        return self.db['schema']
    
    def insert(self, value, overwrite=False, dump_db=False):
        """ Set the key-value pair in the database """
        primary_value = str(value[self.primary_value_index])

        if primary_value in self.db['database'] and not overwrite:
            return False
        
        if len(value) != len(self.columns_list):
            return False
        
        self.db["database"][primary_value] = dict(zip(self.columns_list, value))

        if dump_db:
            self.dump_db()
        return True

    def get_db(self):
        return self.db

    def clear(self):
        self.db = {"database": {}, "schema": {}}
        self.dump_db()
        return True

    def delete(self, primary_value):
        """ Delete the key-value pair in the database """
        if primary_value in self.db['database']:
            del self.db['database'][primary_value]
            self.dump_db()
            return True
        return False
    
    def update(self, primary_value, value):
        """ Update the key-value pair in the database """
        if primary_value in self.db['database']:
            self.db['database'][primary_value] = value
            self.dump_db()
            return True
        return False
    
    def search(self, primary_value):
        """ Search the key-value pair in the database """
        if primary_value in self.db['database']:
            return self.db['database'][primary_value]
        return False
    
    def where(self, column_name, value):
        """ Search the key-value pair in the database """
        result = []
        for key, val in self.db['database'].items():
            if val[column_name] == value:
                result.append(val)
        return result
    
    def __repr__(self):
        return f"QuickDB(db_path={self.db_path}, db={self.db})"
    
    def __str__(self):
        return f"QuickDB(db_path={self.db_path}, db={self.db})"
    
    def __getitem__(self, key):
        return self.db["database"][key] if key in self.db["database"] else None