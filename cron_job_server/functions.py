from pymongo import MongoClient 
import pandas as pd 
import os


def conn_db(): 
    user = os.getenv("DBUSER", 'signature')
    pwd = os.getenv("DBPWD", 'shanekang')
    ip_addr = os.getenv("DBADDR", '54.180.213.105')

    conn = MongoClient(f'mongodb://{user}:{pwd}@{ip_addr}:27017') 
    return conn


def insert_data(df, collection, *chk_keys, check=False): 
    doc_list = list() 
    for _, row in df.iterrows(): 
    
        # Check if duplicated
        if check: 
            query_dict = {k: row[k] for k in chk_keys}
            if collection.find_one(query_dict): continue

        doc = {col: val for col, val in zip(df.columns, row)} 
        doc_list.append(doc)

    if doc_list: 
        collection.insert_many(doc_list)
        return True 

    return False 


def upsert_data(df, collection, keys, upsert_columns=None, reset=False, skip_na=False): 

    if reset: collection.drop() 
    
    if not upsert_columns: 
        upsert_columns = [col for col in df.columns if col not in keys]

    status = False 

    for _, row in df.iterrows(): 

        key_values = [row[elem] for elem in keys]
        upsert_values = [row[elem] for elem in upsert_columns]

        if skip_na and (0 in upsert_values or '0' in upsert_values): continue

        collection.find_one_and_update(
            {k: v for k, v in zip(keys, key_values)}, 
            {'$set': {k: v for k, v in zip(upsert_columns, upsert_values)} }, 
            upsert=True)
        status = True 

    return status


