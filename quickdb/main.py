import os
import json

from colorama import Fore, Style

colors_dict = {
    'red' : Fore.RED,
    'green' : Fore.GREEN,
    'yellow' : Fore.YELLOW,
    'blue' : Fore.BLUE,
    'magenta' : Fore.MAGENTA,
    'cyan' : Fore.CYAN,
    'white' : Fore.WHITE,
    'reset' : Style.RESET_ALL
}


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

    def __print(self, color, text):
        """ Print function to print colored text """
        if self.debug:
            print(colors_dict[color] + text + colors_dict['reset'])

    def __init_db(self):
        """" Initialize the database """
        if not self.overwrite_db and os.path.exists(self.db_path):
            self.__print("green", "Loading database from file")
            return self.__load_db_from_file()

        elif self.overwrite_db and os.path.exists(self.db_path):
            self.__print("blue", "Overwriting database")
            self.clear()
            return self.db

        elif not os.path.exists(self.db_path):
            self.__print("green", "Creating new database")
            return {}
        
    def create_schema(self, columns_list, primary_key):
        """ Create the schema of the database """
        self.schema = {
            "columns": columns_list,
            "primary_key": primary_key
        }
        self.primary_key = primary_key

    def __load_db_from_file(self):
        """ Load the database from the file """
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def __dump_db(self, data):
        """ Dump the database to the file """
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(data, f, indent=4)
                return True
        except Exception:
            return False

    def set(self, value, overwrite=False):
        """ Set the key-value pair in the database """
        primary_value = value[self.schema["columns"].index(self.primary_key)]

        if primary_value in self.db and not overwrite:
            self.__print("red", "Key already exists")
            return False
        
        if self.primary_key not in self.schema["columns"] or len(value) != len(self.schema["columns"]):
            self.__print("red", "Invalid column name or number of columns")
            return False

        self.db[primary_value] = dict(zip(self.schema["columns"], value))
        self.__dump_db(self.db)
        return True

    def get_db(self):
        return self.db

    def clear(self):
        self.db = {}
        self.__dump_db(self.db)
        self.__print("green", "Database cleared")
        return True
