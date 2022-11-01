from quickdb.main import QuickDB

db = QuickDB("test_db.json", overwrite_db=True)
db.set("name", "John")
db.set("age", 25)
db.set("age", 30, overwrite=True)
print(db.get("name"))
print(db.get("age"))

db.get_db()