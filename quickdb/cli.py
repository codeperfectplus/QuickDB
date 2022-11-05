import argparse
import sys

sys.path.append(".")
from quickdb import QuickDB

version = "quickdb 0.0.2"

argparse = argparse.ArgumentParser(description="QuickDB CLI")
argparse.add_argument("--debug", action="store_true", help="Enable debug mode")
argparse.add_argument("-p", "--db_path", help="Path to the database file", required=True)
argparse.add_argument("-o", "--overwrite", help="Overwrite the database", action="store_true")
argparse.add_argument('-v', '--version', action='version', version=version)

group = argparse.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--set", help="Set a key-value pair in the database")
group.add_argument("-g", "--get", help="Get a value from the database")
group.add_argument("-d", "--delete", help="Delete a key-value pair from the database")
group.add_argument("-c", "--clear", help="Clear the database", action="store_true")
args = argparse.parse_args()

debug = True if args.debug else False

db = QuickDB(args.db_path, overwrite_db=False, debug=debug)


def main():
    if args.set:
        key, value = args.set.split("=")
        if args.overwrite:
            db.set(key, value, overwrite=True)
        else:
            db.set(key, value)
    elif args.get:
        key = args.get
        print(db.get(key))
    elif args.delete:
        key = args.delete
        db.delete(key)
    elif args.clear:
        db.clear()
    else:
        print("Invalid arguments")
        # check if the command is similar to any of the commands


if __name__ == "__main__":
    main()
