Command line Usages
==================

.. code-block:: bash

    --debug Enable debug mode
    -v, --version         show program's version number and exit
    -p  path to the database 

    -s SET, --set SET     Set a key-value pair in the database
    -g GET, --get GET     Get a value from the database
    -d DELETE, --delete DELETE
                            Delete a key-value pair from the database
    -c, --clear           Clear the database

    -o --overwrite        to overwrite the value if the key already exists

Set a key-value pair in the database

.. code-block:: bash
    quickdb -p test.db -s key=value

    # if the key already exists, overwrite the value by adding the -o flag
    quickdb -p test.db -s key=value -o

Get a value from the database

.. code-block:: bash
    quickdb -p test.db -g key

Delete a key-value pair from the database

.. code-block:: bash
    quickdb -p test.db -d key


Clear the database

.. code-block:: bash
    quickdb -p test.db -c

use --debug to enable debug mode with colored output
