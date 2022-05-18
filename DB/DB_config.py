from pymongo import MongoClient
from const.const import MONGODB_CONNECTION

class MongoDB:

    def __init__(self, db_name, collection):
        try:
            self.db_name = db_name
            self.collection = collection
            self.client = MongoClient(MONGODB_CONNECTION)
            self.mongo_con = self.client[self.db_name]
            self.collection = self.mongo_con[self.collection]
            print("Mongo DB connection successfull \n")
        except:
            print("Mongo DB connection unsuccessfull \n")
    
    def insert_into(self, object):
        res = self.collection.insert_one(object)
        return res
    
    def get_records(self):
        cursor = self.collection.find()
        records = []
        for record in cursor:
            records.append(record)
        
        return records