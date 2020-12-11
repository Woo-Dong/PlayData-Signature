from pymongo import MongoClient
import pymongo


from datetime import datetime
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

    diff = list() 
    for i in range(len(ret_df)): 
        row = ret_df.iloc[i] 
        diff.append(abs(row.real-row.pred))
    
    minimum, maximum = diff[0], diff[0] 
    min_date, max_date = '', '' 
    for idx, elem in enumerate(diff): 
        if elem <= minimum: 
            minimum = elem 
            min_date = ret_df.iloc[idx].date 
        if elem >= maximum: 
            maximum = elem 
            max_date = ret_df.iloc[idx].date 
    min_value = min_date.strftime("%Y-%m-%d") + '일 => ' + str(minimum)
    max_value = max_date.strftime("%Y-%m-%d") + '일 => ' + str(maximum)
    average = int(sum(diff)/len(diff)) 

    return ret_df, min_value, average, max_value



def get_global_daily_data(): 

    conn = conn_db() 
    daily_collections = conn.GlobalCOVID.daily
    columns = ['date', 'country', 'confirmed', 'deaths', 'recovered']

    total_data =[ [elem[col] for col in columns] for elem in daily_collections.find({}) ]
    conn.close() 

    ret_df = pd.DataFrame(total_data, columns=columns)
    ret_df = ret_df[['date', 'country', 'confirmed']]
    ret_df['date'] = pd.to_datetime(ret_df['date'])

    return ret_df


def get_global_cumul_data(): 

    conn = conn_db() 
    cumul_collections = conn.GlobalCOVID.cumul

    last_date = cumul_collections.find_one({}, 
                    sort=[( '_id', pymongo.DESCENDING )]
                )['date']

    columns = ['date', 'country', 'confirmed', 'deaths', 'recovered']
    total_data = [[elem[col] for col in columns] for elem in cumul_collections.find(
                                                {'date': last_date})]
    conn.close() 

    ret_df = pd.DataFrame(total_data, columns=columns)
    ret_df.drop('date', axis=1, inplace=True)
    ret_df.sort_values('confirmed', ascending=True, inplace=True)

    return ret_df, last_date



def get_domestic_daily_data(key): 
    
    conn = conn_db() 
    domestic_detailed_collection = conn.DomesticDetailedCOVID[key]

    col_list = ['date', key, 'confirmed', 'death']
    total_data = [[elem[col] for col in col_list] for elem in domestic_detailed_collection.find({})]

    conn.close() 
    ret_df = pd.DataFrame(total_data, columns=col_list) 
    ret_df.sort_values(['date', key], inplace=True)
    n = len(ret_df[key].unique()) * 7
    if len(ret_df) > n: ret_df = ret_df.tail(n) 

    ret_df.confirmed = ret_df.confirmed.astype(int)
    ret_df.death = ret_df.death.astype(int)
    ret_df = ret_df[ret_df['date'] > '2020-04-09']

    tmp = ret_df[[key, 'confirmed']].groupby(key).sum() 
    
    maximum = tmp.loc[tmp['confirmed'].idxmax()]
    max_name, max_value = maximum.name, str(maximum.values[0])
    maximum = f'{maximum.name}: {max_value}명'


    minimum = tmp.loc[tmp['confirmed'].idxmin()]
    max_name, min_value = minimum.name, str(minimum.values[0])
    minimum = f'{minimum.name}: {min_value}명'


    return ret_df, maximum, minimum


def get_domestic_cumul_data(key): 
    conn = conn_db() 

    domestic_detailed_cumul_collection = conn.DomesticDetailedCOVID.cumul
    col_list = ['attr', 'confirmed', 'death', 'isolated', 'released']
    

    def _set_df_input_data(col_list, collection, query): 

        cursor = collection.find({'type': query})
        total_data = list() 
        for elem in cursor: 
            tmp = list() 
            for col in col_list: 
                if type(elem[col]) == str: tmp.append(elem[col].replace(',', ''))
                else: tmp.append(elem[col])
            total_data.append(tmp) 
        return total_data
    
    if key == 'area': 
    
        total_data = _set_df_input_data(col_list, domestic_detailed_cumul_collection, 'area') 
        area_df = pd.DataFrame(total_data, columns=col_list) 
        area_df = area_df[area_df['attr'] != '소계']
        area_df = area_df[area_df['attr'] != '검역']

        for col in col_list[1:]: area_df[col] = area_df[col].astype(int)
        area_df.sort_values('confirmed', ascending=True, inplace=True) 
        
        return area_df 

    col_list = col_list[:3] # ['attr', 'confirmed', 'death']

    if key == 'age': 

        total_data = _set_df_input_data(col_list, domestic_detailed_cumul_collection, 'age') 
        age_df = pd.DataFrame(total_data, columns=col_list) 

        for col in col_list[1:]: age_df[col] = age_df[col].astype(int)
        age_df.sort_values('attr', ascending=True, inplace=True) 

        return age_df

    total_data = _set_df_input_data(col_list, domestic_detailed_cumul_collection, 'gender') 
    gender_df = pd.DataFrame(total_data, columns=col_list) 
    gender_df.sort_values('attr', inplace=True)

    for col in col_list[1:]: gender_df[col] = gender_df[col].astype(int)

    return gender_df 

def get_news_summary(): 

    conn = conn_db()
    cluster_summary_collection = conn.NewsData.cluster_summary
    
    # result = news_db.find().sort("date", -1).limit(3) 
    summaries = cluster_summary_collection.find({}) 

    results = [elem['content'] for elem in summaries]

    conn.close() 

    return results

def get_brefing_info(): 

    conn = conn_db() 
    brefing_info_collection = conn.NewsData.brefing_info 

    summaries = brefing_info_collection.find({}) 

    columns = ['title', 'date', 'contents']
    result = [{col: elem[col] for col in columns} for elem in summaries]

    return result[0] 

    