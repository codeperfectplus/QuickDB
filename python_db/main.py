import os
import json
import re

from colorama import Fore, Style

def print_it(color, text):
    if color == "red":
        print(Fore.RED + text + Style.RESET_ALL)
    elif color == "green":
        print(Fore.GREEN + text + Style.RESET_ALL)
    elif color == 'blue':
        print(Fore.BLUE + text + Style.RESET_ALL)

class Database(object):
    """  python database.py """
    def __init__(self, db_path, overwrite_db=False):
        self.db_path = db_path
        self.db = self.__init_db(overwrite_db)

    def __load_db_from_file(self):
        with open(self.db_path, 'r') as f:
            return json.load(f)
    
    def __init_db(self, overwrite_db):
        if not overwrite_db and os.path.exists(self.db_path):
            print_it("green", "Loading database from file")
            return self.__load_db_from_file()
            
        elif overwrite_db and os.path.exists(self.db_path):
            print_it("blue", "Overwriting database")
            self.clear()
            return self.db
        
        elif not os.path.exists(self.db_path):
            print_it("green", "Creating new database")
            return {}

    def __dump_db(self, data):
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(data, f, indent=4)
                return True
        except Exception as e:
            return False

    def set(self, key, value, overwrite=False):
        if key not in self.db:
            print_it("green", "Key is not present in the database, adding in the database")

            self.db[key] = value
            self.__dump_db(self.db)
            return True
        
        elif not overwrite and key in self.db:
            print_it("red", "Key already exists")
            return False
    
        elif overwrite and key in self.db:
            print_it("blue", "Key already exists, overwriting the value")
            self.db[key] = value
            self.__dump_db(self.db)
            return True

    def get(self, key):
        if key in self.db:
            return self.db[key]
        else:
            print_it("red", "Key not found")
            return False
    
    def delete(self, key):
        if key in self.db:
            del self.db[key]
            self.__dump_db(self.db)
            print_it("green", "Key deleted")
        else:
            print_it("red", "Key not found")

    def get_db(self):
        print(self.db)
        return self.db
    
    def clear(self):
        self.db = {}
        self.__dump_db(self.db)
        print_it("green", "Database cleared")
        return True

