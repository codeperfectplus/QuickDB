from ast import For
import os
import json

from colorama import Fore
from colorama import Style

def print_it(color, text):
    if color == "red":
        print(Fore.RED + text + Style.RESET_ALL)
    elif color == "green":
        print(Fore.GREEN + text + Style.RESET_ALL)
    elif color == 'blue':
        print(Fore.BLUE + text + Style.RESET_ALL)

class Database(object):
    """  python database.py """
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = self.load_db()

    def load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_db(self, data):
        with open(self.db_path, 'w+') as f:
            try:
                json.dump(data, f, indent=4)
                return True
            except Exception as e:
                return False

    def set(self, key, value, overwrite=False):

        if key not in self.db:
            print_it("green", "Key is not present in the database, adding in the database")
            self.db[key] = value
            self.save_db(self.db)
        
        elif not overwrite and key in self.db:
            print_it("red", "Key already exists")
    
        elif overwrite and key in self.db:
            print_it("blue", "Key already exists, overwriting the value")
            self.db[key] = value
            self.save_db(self.db)

    def get(self, key):
        if key in self.db:
            return self.db[key]
        else:
            print_it("red", "Key not found")
            return False

    def delete_db(self):
        os.remove(self.db_path)
        print_it("green", "Database deleted")
        
    
    def delete(self, key):
        if key in self.db:
            del self.db[key]
            self.save_db(self.db)
            print_it("green", "Key deleted")
        else:
            print_it("red", "Key not found")
            
    
    def list(self):
        return self.db
    
    def clear(self):
        self.db = {}
        self.save_db(self.db)
        print_it("green", "Database cleared")
        
    

if __name__ == '__main__':
    db = Database('db.json')
    data = db.load_db()
    db.set('key', 'value', overwrite=True)
    out = db.list()
    print(out)
    db.clear()
