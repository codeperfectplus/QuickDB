import sys
sys.path.append('.')
import unittest

from src.main import Database

db = Database("test_db.json", overwrite_db=True)

class DatabaseTest(unittest.TestCase):
    
    def test_operation_one(self):
        """ if key does not exist, it should be added """
        self.assertTrue(db.set("name", "john"))
        self.assertTrue(db.set("age", 25))
        self.assertTrue(db.set("age", 30, overwrite=True))
        self.assertEqual(db.get_db(), {'name': 'john', 'age': 30})
        self.assertTrue(db.clear(), True)
    
    def test_operation_two(self):
        """ if key already exists, it should not be added """
        self.assertTrue(db.set("name", "john"))
        self.assertFalse(db.set("name", "john"))
        self.assertTrue(db.clear(), True)
        
    def test_operation_three(self):
        """ if key already exists, it should be overwritten """
        self.assertTrue(db.set("name", "john"))
        self.assertTrue(db.set("name", "john", overwrite=True))
        self.assertTrue(db.clear(), True)
    
    
    
if __name__ == '__main__':
    unittest.main()