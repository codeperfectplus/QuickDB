Use as library
==============

```
from quickdb import QuickDB
```

Initialize the database
------------------------

```
db_object = QuickDB(db_path="quickdb.json")
```

Create a table
--------------

It will create a table schema with the given columns and primary key. 
If the table already exists, it will not create a new table.

```
table_name = 'employee'
columns = ['serial', 'name', 'age', 'city', 'country', 'email', 'phone', 'salary']
primary_key = 'serial'
db_object.create_table(table_name, columns, primary_key)
```

Insert data
-----------

It will insert the data into the table. if primary_key is already present, it will not insert the data.
overwrite need to pass as True to overwrite the data.

```
db_object.insert_into(table_name=table_name,
    value=[1, 'John Doe', 30, 'New York', 'USA', 'john@gmail.com', '1234567890', 50000], commit=True)
db_object.insert_into(table_name=table_name,
    value=[1, 'John Doe', 30, 'New York', 'USA', 'john@gmail.com', '1234567890', 50000], commit=True, overwrite=True)
db_object.dump_db() # Save the data to the file
```

Insert multiple data
--------------------

If you want to insert multiple data at once, you can use the below method.

```
# insert_into_many
values = [
    [3, 'John Doe', 30, 'New York', 'USA', 'd@gmail.com', '1234567890', 50000],
    [4, 'John Doe', 30, 'New York', 'USA', 'f@gs', '1234567890', 50000]
]
db_object.insert_into_many(table_name=table_name, values=values, commit=True)
```
