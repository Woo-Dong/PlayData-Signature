from functions import conn_db, insert_data, upsert_data, train_FBProphet_model

import pandas as pd 
import os, io


def predict_FBProphet_model(): 

    conn = conn_db() 
    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul

    total_data = [[elem['date'], elem['confirmed']] for elem in domestic_cumul_collection.find({})]
    conn.close() 

    prev_num = total_data[-1]

    model = train_FBProphet_model(total_data) 

    future = model.make_future_dataframe(periods=7) 
    forecast = model.predict(future) 

    forecast = forecast.iloc[-7:, :]

    forecast['yhat'] = forecast['yhat'].astype(int)

    ret_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    ret_df.rename({'ds': 'date'}, axis=1, inplace=True) 
    ret_df['date'] = ret_df['date'].apply(lambda x:str(x).split()[0]) 

    return ret_df, prev_num


def validate_FBProphet_model(ADJ_CONST): 

    conn = conn_db() 
    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul 

    total_data = [[elem['date'], elem['confirmed']] for elem in domestic_cumul_collection.find({})]
    conn.close() 

    train_data = total_data[:-7]
    prev_num = total_data[-8][1] 

    val_data = [(elem[1]-prev_num) for elem in total_data[-7:]]



    model = train_FBProphet_model(train_data) 

    future = model.make_future_dataframe(periods=7) 
    forecast = model.predict(future) 

    result = forecast.tail(7) 
    col_list = ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
    result = result[col_list]
    result.rename({'ds': 'date'}, axis=1, inplace=True) 
    result.date = result.date.apply(lambda x: x.strftime("%Y-%m-%d"))

    for col in col_list[1:]: result[col] = round((result[col] - prev_num) * ADJ_CONST, 0)
    result['real'] = val_data 

    return result 


def upsert_inference_data(): 

    pred_df, prev_num = predict_FBProphet_model()
    conn = conn_db()
    inference_FBProphet_collection = conn.DomesticCOVID.inference_FBProphet
    
    upsert_data(pred_df, inference_FBProphet_collection, ['date'], reset=True)

    prev_doc = { 
        'date': prev_num[0], 
        'real': prev_num[1]
    }
    inference_FBProphet_collection.insert(prev_doc) 
    conn.close() 

    return True


def insert_validate_FBProphet_data(ADJ_CONST=1.4): 

    try: 
        val_df = validate_FBProphet_model(ADJ_CONST) 

        conn = conn_db() 

        validate_FBProphet_collection = conn.DomesticCOVID.validate_FBProphet 
        validate_FBProphet_collection.drop()

        col_list = val_df.columns 
        doc_list = list() 

        insert_data(val_df, validate_FBProphet_collection, check=False)

        conn.close() 
        return True 

    except: 
        print("Error Occured: insert_validate_FBProphet_data Function")
        return False 


if __name__ == "__main__":
    print("predict FBProphet data Upsert: ", upsert_inference_data())
    print("validate FBPropeht data Insert: ", insert_validate_FBProphet_data(ADJ_CONST=1.7))
     