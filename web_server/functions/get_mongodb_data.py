from pymongo import MongoClient

import plotly.graph_objs as go 
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

    inference_fbprophet_collection = conn.DomesticCOVID.inference_FBProphet

    col_list = ['date', 'yhat', 'yhat_lower', 'yhat_upper']
    total_data = inference_fbprophet_collection.find({})
    prev = total_data[7]
    total_data = [[elem[k] for k in col_list] for elem in total_data[:7]] 
    conn.close() 

    conv_colnames = ['date', 'pred', 'lower', 'upper']
    pred_df = pd.DataFrame(total_data, columns=conv_colnames) 

    pred_df['date'] = pd.to_datetime(pred_df['date'])

    return pred_df, prev['real']

def get_validate_fbprophet_data(): 

    conn = conn_db() 

    validate_FBProphet_collection = conn.DomesticCOVID.validate_FBProphet
    
    col_list = ['date', 'yhat', 'yhat_lower', 'yhat_upper', 'real']

    total_data = [[elem[k] for k in col_list] for elem in validate_FBProphet_collection.find({})] 

    conn.close() 
    conv_colnames = ['date', 'pred', 'lower', 'upper', 'real']
    ret_df = pd.DataFrame(total_data, columns=conv_colnames) 

    ret_df['date'] = pd.to_datetime(ret_df['date'])

    return ret_df 


def get_news_data(): 

    news_db = conn_db('news')
    result = news_db.find().sort("date", -1).limit(3) 
    result = list(result)
    res = result[0] 
    del(res['_id'])

    return res