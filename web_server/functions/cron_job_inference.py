
from pymongo import MongoClient
from fbprophet import Prophet
import pandas as pd 

def conn_db(collection): 
    MONGO_URI = "mongodb://{dbuser}:{dbpassword}@ds253918.mlab.com:53918/signature"
    MONGO_URI = MONGO_URI.format(dbuser='admin', dbpassword='user123')

    conn = MongoClient(MONGO_URI, retryWrites="false")
    db = conn.get_default_database()
    ret_db = db[collection]

    return ret_db


def predict_fbprophet(collection): 

    confirmed_db = conn_db(collection) 

    total_data = [[elem['date'], elem['confirmed']] for elem in confirmed_db.find({})]


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
    forecast['trend'] = forecast['trend'].astype(int)

    ret_df = forecast[['ds', 'trend']]
    ret_df.rename({'ds': 'date'}, axis=1, inplace=True) 
    return ret_df


# insert_inference_data(predict_fbprophet('sample'))
def insert_inference_data(): 

    data_df = predict_fbprophet('sample')

    result_db = conn_db('predFBProphet')

    doc_list = list() 

    for _, row in data_df.iterrows(): 
        doc = {col: None for col in data_df.columns} 
    
        doc['date'] = str(row[0]).split()[0]
        doc['trend'] = row[1]
        result_db.find_one_and_update({'date': doc['date']}, 
                            {'$set': {'trend': doc['trend']}}, 
                            upsert=True)
    return True
