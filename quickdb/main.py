import os
import json

from colorama import Fore, Style


class QuickDB(object):
    """  python database.py """
    def __init__(self, db_path, overwrite_db=False, debug=True):
        self.db_path = db_path
        self.debug = debug
        self.overwrite_db = overwrite_db
        self.db = self.__init_db()
        self.schema = None
        self.primary_key = None
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

    def __dump_db(self, data):
        """ Dump the database to the file """
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(data, f, indent=4)
                return True
        except json.JSONDecodeError:
            return False
    
    def create_schema(self, columns_list, primary_key):
        """ Create the schema of the database """
        self.primary_key = primary_key
        self.columns_list = columns_list
        self.primary_value_index = self.columns_list.index(self.primary_key)

    def set(self, value, overwrite=False):
        """ Set the key-value pair in the database """
        primary_value = value[self.primary_value_index]

        if primary_value in self.db and not overwrite:
            return False
        
        if self.primary_key not in self.columns_list or len(value) != len(self.columns_list):
            return False

        self.db[primary_value] = dict(zip(self.columns_list, value))
        self.__dump_db(self.db)
        return True

    def get_db(self):
        return self.db

    def clear(self):
        self.db = {}
        self.__dump_db(self.db)
        return True
