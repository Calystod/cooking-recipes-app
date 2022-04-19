from pymongo import MongoClient
import os

def get_client():
    client = MongoClient(
      "mongodb+srv://" + os.environ['DB_USER'] + ":" + os.environ['DB_PASSWORD'] + "@" + os.environ['DB_SERVER'] + "/" + os.environ['DB_NAME'] + "?retryWrites=true&w=majority")

    db = client.cooking_db

    return db

def add(key, document):
    db = get_client()

    my_collection = db[key]

    id_element = my_collection.insert_one(document)

    return id_element

def get(key, filters):
    db = get_client()
    my_collection = db[key]

    element = my_collection.find_one(filters)

    return element

def get_multi(key, filters):
    db = get_client()
    my_collection = db[key]

    elements = my_collection.find(filters)

    return elements

def delete(key, filters):
    db = get_client()
    my_collection = db[key]

    return my_collection.delete_one(filters).deleted_count
