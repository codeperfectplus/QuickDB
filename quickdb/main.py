import os
import json

from colorama import Fore, Style


class QuickDB(object):
    """  python database.py """
    def __init__(self, db_path, overwrite_db=False, print_output=True):
        self.db_path = db_path
        self.print_output = print_output
        self.db = self.__init_db(overwrite_db)

    def print_it(self, color, text, print_output=True):
        if self.print_output:
            if color == "red":
                print(Fore.RED, text)
            elif color == "green":
                print(Fore.GREEN, text)
            elif color == 'blue':
                print(Fore.BLUE, text)
            print(Style.RESET_ALL, end='')

    def __load_db_from_file(self):
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def __init_db(self, overwrite_db):
        if not overwrite_db and os.path.exists(self.db_path):
            self.print_it("green", "Loading database from file")
            return self.__load_db_from_file()

        elif overwrite_db and os.path.exists(self.db_path):
            self.print_it("blue", "Overwriting database")
            self.clear()
            return self.db

        elif not os.path.exists(self.db_path):
            self.print_it("green", "Creating new database")
            return {}

    def __dump_db(self, data):
        try:
            with open(self.db_path, 'w+') as f:
                json.dump(data, f, indent=4)
                return True
        except Exception:
            return False

    def set(self, key, value, overwrite=False):
        if key not in self.db:
            self.print_it("green", "Key is not present in the database, adding in the database")

            self.db[key] = value
            self.__dump_db(self.db)
            return True

        elif not overwrite and key in self.db:
            self.print_it("red", "Key already exists")
            return False

        elif overwrite and key in self.db:
            self.print_it("blue", "Key already exists, overwriting the value")
            self.db[key] = value
            self.__dump_db(self.db)
            return True

    def get(self, key):
        if key in self.db:
            return self.db[key]
        else:
            self.print_it("red", "Key not found")
            return False

    def delete(self, key):
        if key in self.db:
            del self.db[key]
            self.__dump_db(self.db)
            self.print_it("green", "Key deleted")
        else:
            self.print_it("red", "Key not found")

    def get_db(self):
        print(self.db)
        return self.db

    def clear(self):
        self.db = {}
        self.__dump_db(self.db)
        self.print_it("green", "Database cleared")
        return True
