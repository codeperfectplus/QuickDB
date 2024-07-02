import unittest
import sys

sys.path.append(".")

from quickdb.main import QuickDB
db = QuickDB("test_db.json", overwrite_db=True)


class DatabaseTest(unittest.TestCase):
    
    def test_create_table(self):
        table_name = 'employee'
        columns = ['serial', 'name', 'age', 'city', 'country', 'email', 'phone', 'salary']
        primary_key = 'serial'
        db.create_table(table_name, columns, primary_key)
        self.assertEqual(db.get_table_columns(table_name), columns)

    def test_get_table_names(self):
        table_name = 'employee'
        self.assertEqual(db.get_table_names(), [table_name])

    def test_get_table(self):
        table_name = 'employee'
        columns = ['serial', 'name', 'age', 'city', 'country', 'email', 'phone', 'salary']
        primary_key = 'serial'
        self.assertEqual(db.get_table(table_name), {"columns_list": columns, 
                                                    "primary_key": primary_key, 
                                                    "primary_key_index": 0})

    def test_get_table_primary_key(self):
        table_name = 'employee'
        primary_key = 'serial'
        self.assertEqual(db.get_table_primary_key(table_name), primary_key)

    def test_insert_into(self):
        table_name = 'employee'
        db.insert_into(table_name=table_name,
                        value=[1, 'John Doe', 30, 'New York', 'USA', 'd@mail.com', '1234567890', 50000], commit=True)
        self.assertEqual(len(db.get_table_data(table_name)), 1)

    def test_drop_table(self):
        table_name = 'student'
        columns = ['roll', 'name', 'age', 'city', 'country', 'email', 'phone', 'fees']
        primary_key = 'roll'
        db.create_table(table_name, columns, primary_key)
        self.assertEqual(db.get_table_names(), ['employee', 'student'])
        db.drop_table(table_name)
        self.assertEqual(db.get_table_names(), ['employee'])

    def test_clear_database(self):
        db.clear_database()
        self.assertEqual(db.get_db(), {"database": {}, "schema": {}})

if __name__ == '__main__':
    unittest.main()
