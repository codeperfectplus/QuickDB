import unittest
import sys

sys.path.append(".")

from quickdb.main import QuickDB

db = QuickDB("test_db.json", overwrite_db=True)


class DatabaseTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
