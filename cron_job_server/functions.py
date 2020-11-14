from pymongo import MongoClient 
import os


def conn_db(): 
    user = os.getenv("DBUSER", '')
    pwd = os.getenv("DBPWD", '')
    ip_addr = os.getenv("DBADDR", '')

    conn = MongoClient(f'mongodb://{user}:{pwd}@{ip_addr}:27017') 
    return conn


def insert_data(df, collection, *chk_keys): 
    doc_list = list() 
    for _, row in df.iterrows(): 
    
        # Check if duplicated
        query_dict = {k: row[k] for k in chk_keys}
        if collection.find_one(query_dict): continue

        doc = {col: val for col, val in zip(df.columns, row)} 
        doc_list.append(doc)

    if doc_list: 
        collection.insert_many(doc_list)
        return True 

    return False 

# TODO 
def upsert_data(df, collection, key, set_col): 
    pass 