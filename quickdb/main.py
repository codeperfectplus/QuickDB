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
        self.db = self.__init_db(overwrite_db)

    def __print(self, color, text):
        """ Print function to print colored text """
        if self.debug:
            print(colors_dict[color] + text + colors_dict['reset'])

    def __load_db_from_file(self):
        """ Load the database from the file """
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def __init_db(self, overwrite_db):
        """" Initialize the database """
        if not overwrite_db and os.path.exists(self.db_path):
            self.__print("green", "Loading database from file")
            return self.__load_db_from_file()

        elif overwrite_db and os.path.exists(self.db_path):
            self.__print("blue", "Overwriting database")
            self.clear()
            return self.db

        elif not os.path.exists(self.db_path):
            self.__print("green", "Creating new database")
            return {}

    def __dump_db(self, data):
        """ Dump the database to the file """
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(data, f, indent=4)
                return True
        except Exception:
            return False

    def set(self, key, value, overwrite=False):
        if key not in self.db:
            self.__print("green", "Key is not present in the database, adding in the database")

            self.db[key] = value
            self.__dump_db(self.db)
            return True

        elif not overwrite and key in self.db:
            self.__print("red", "Key already exists")
            return False

        elif overwrite and key in self.db:
            self.__print("blue", "Key already exists, overwriting the value")
            self.db[key] = value
            self.__dump_db(self.db)
            return True

    def get(self, key):
        if key in self.db:
            return self.db[key]
        else:
            self.__print("red", "Key not found")
            return False

    def delete(self, key):
        if key in self.db:
            del self.db[key]
            self.__dump_db(self.db)
            self.__print("green", "Key deleted")
        else:
            self.__print("red", "Key not found")

    def get_db(self):
        print(self.db)
        return self.db

    def clear(self):
        self.db = {}
        self.__dump_db(self.db)
        self.__print("green", "Database cleared")
        return True
