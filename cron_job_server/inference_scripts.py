
from fbprophet import Prophet
import pandas as pd 
import os, io

from functions import conn_db, insert_data 


def predict_fbprophet(): 

    conn = conn_db() 
    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul

    total_data = [[elem['date'], elem['confirmed']] for elem in domestic_cumul_collection.find({})]

    conn.close() 

    prophet_df = pd.DataFrame(total_data, columns=['ds', 'y'])
    prophet_df.sort_values('ds', inplace=True)

    model = Prophet( 
        changepoint_prior_scale=.2, # increasing it will make the trend more flexible
        changepoint_range=.98, # place potential changepoints in the 98% of the time series
        yearly_seasonality=False, 
        weekly_seasonality=True, 
        daily_seasonality=True,
        seasonality_mode='additive'
    )

    model.fit(prophet_df) 

    future = model.make_future_dataframe(periods=7) 
    forecast = model.predict(future) 
    forecast['yhat'] = forecast['yhat'].astype(int)

    ret_df = forecast[['ds', 'yhat']]
    ret_df.rename({'ds': 'date'}, axis=1, inplace=True) 
    ret_df['date'] = ret_df['date'].apply(lambda x:str(x).split()[0]) 

    return ret_df

def upsert_inference_data(): 

    pred_df = predict_fbprophet()
    conn = conn_db()
    inference_fbprophet_collection = conn.DomesticCOVID.inference_fbprophet

    for _, row in pred_df.iterrows(): 
        doc = {col: None for col in pred_df.columns} 
    
        doc['date'] = row[0] 
        doc['yhat'] = row[1]
        inference_fbprophet_collection.find_one_and_update(
                                            {'date': doc['date']}, 
                                            {'$set': {'yhat': doc['yhat']}}, 
                                            upsert=True)

    conn.close() 
    return True


if __name__ == "__main__":
    print("Status: ", upsert_inference_data())
     
     