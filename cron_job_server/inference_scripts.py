from fbprophet import Prophet
import pandas as pd 
import os, io


from functions import conn_db, insert_data, upsert_data



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


def insert_validate_FBProphet_data(ADJ_CONST=1.): 
    print("ADJ_CONST(R0): ", ADJ_CONST)

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

def get_R0(): 
    conn = conn_db()
    data = conn.DomesticDetailedCOVID.cumul.find({'attr': '소계'})[0]
    conn.close() 
    
    # Confirmed, Death, Released
    tmp = [data['confirmed'], data['death'], data['released']]
    for i in range(3): tmp[i] = tmp[i].replace(',' ,'')
    I, D, R = map(int, tmp)
    R += D 
    gamma = 1/14
    gamma = round(gamma, 2)
    beta = 0.1389
    
    TOTAL = 51780579
    
    S = (TOTAL - I)
    s = (S/(S+I+R))
    Ro = (beta*s) / gamma
    Ro = round(Ro, 3)
    
    return Ro

if __name__ == "__main__":
    print("predict FBProphet data Upsert: ", upsert_inference_data())
    print("validate FBPropeht data Insert: ", insert_validate_FBProphet_data(ADJ_CONST=get_R0()))
     