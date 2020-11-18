from pymongo import MongoClient 
from fbprophet import Prophet
import pandas as pd 
import os


def conn_db(): 
    user = os.getenv("DBUSER", 'signature')
    pwd = os.getenv("DBPWD", 'shanekang')
    ip_addr = os.getenv("DBADDR", '54.180.213.105')

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


def train_FBProphet_model(data, 
                        changepoint_prior_scale=.2,  changepoint_range=.98, 
                        yearly_seasonality=False, weekly_seasonality=True, 
                        daily_seasonality=True, seasonality_mode='additive'): 

    prophet_df = pd.DataFrame(data, columns=['ds', 'y'])
    prophet_df.sort_values('ds', inplace=True)

    model = Prophet(
        changepoint_prior_scale=changepoint_prior_scale, # increasing it will make the trend more flexible
        changepoint_range=changepoint_range, # place potential changepoints in the 98% of the time series
        yearly_seasonality=yearly_seasonality, 
        weekly_seasonality=weekly_seasonality, 
        daily_seasonality=daily_seasonality,
        seasonality_mode=seasonality_mode)

    model.fit(prophet_df) 

    return model 

# TODO 
def upsert_data(df, collection, key, set_col): 
    pass 