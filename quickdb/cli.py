from quickdb import QuickDB
import argparse

argparse = argparse.ArgumentParser(description="QuickDB CLI")
argparse.add_argument("-p", "--db_path", help="Path to the database file", required=True)

group = argparse.add_mutually_exclusive_group(required=True)
group.add_argument("-s", "--set", help="Set a key-value pair in the database")
group.add_argument("-g", "--get", help="Get a value from the database")
group.add_argument("-d", "--delete", help="Delete a key-value pair from the database")
group.add_argument("-c", "--clear", help="Clear the database", action="store_true")
args = argparse.parse_args()

db = QuickDB(args.db_path, overwrite_db=False, print_output=True)


def main():
    if args.set:
        key, value = args.set.split("=")
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
