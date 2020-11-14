from pymongo import MongoClient
import pandas as pd 
import os 


def conn_db(): 
    user = os.getenv("DBUSER", '')
    pwd = os.getenv("DBPWD", '')
    ip_addr = os.getenv("DBADDR", '')

    conn = MongoClient(f'mongodb://{user}:{pwd}@{ip_addr}:27017') 
    return conn


def get_dashboard_data(): 

    conn = conn_db() 
    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul 

    result = domestic_cumul_collection.find().sort("date", -1).limit(2)

    conn.close() 

    today, yesterday = list(result)

    col_list = ['confirmed', 'released', 'death']
    today_col = 'today_'
    res_dict = dict() 
    for elem in col_list: 
        new_colname = today_col + elem
        res_dict[new_colname] = today[elem] - yesterday[elem] 
        res_dict[elem] = today[elem]
    res_dict['date'] = today['date']

    return res_dict

def get_confirmed_data(): 

    conn = conn_db() 

    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul 

    total_data = [[elem['date'], elem['confirmed']] for elem in domestic_cumul_collection.find({})]

    conn.close() 

    confirmed_df = pd.DataFrame(total_data, columns=['date', 'confirmed'])
    confirmed_df['date'] = pd.to_datetime(confirmed_df['date'])

    return confirmed_df


def get_predict_fbprophet_data(): 

    conn = conn_db() 

    inference_fbprophet_collection = conn.DomesticCOVID.inference_fbprophet

    total_data = [[elem['date'], elem['yhat']] for elem in inference_fbprophet_collection.find({})]

    pred_df = pd.DataFrame(total_data, columns=['date', 'yhat'])
    pred_df['date'] = pd.to_datetime(pred_df['date'])

    return pred_df


def get_news_data(): 

    news_db = conn_db('news')
    result = news_db.find().sort("date", -1).limit(3) 
    result = list(result)
    
    res = result[0] 
    del(res['_id'])
    return res

