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


def predict_FBProphet_model(ADJ_CONST=1.): 

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
    
    col_list = ['date', 'yhat', 'yhat_lower', 'yhat_upper'] 

    for col in col_list[1:]: ret_df[col] = round((ret_df[col]-prev_num[-1]) * ADJ_CONST, 0)

    
    ret_df['lower_ratio'] = ret_df.yhat_lower / ret_df.yhat 
    ret_df['upper_ratio'] = ret_df.yhat_upper / ret_df.yhat 


    adj_yhat = [ret_df.iloc[0].yhat]
    lower, upper = [ret_df.iloc[0].yhat_lower*1.1], [ret_df.iloc[0].yhat_upper*0.9]
    for i in range(1, len(ret_df)): 
        prev, cur = ret_df.iloc[i-1], ret_df.iloc[i] 
        diff = cur.yhat-prev.yhat
        adj_yhat.append(diff)
        lower.append(diff * cur.lower_ratio)
        upper.append(diff * cur.upper_ratio)
        
    ret_df['yhat'] = adj_yhat 
    ret_df['yhat_lower'] = lower 
    ret_df['yhat_upper'] = upper 
    ret_df.drop(['lower_ratio', 'upper_ratio'], axis=1, inplace=True)

    prev_num[1] = 0
    return ret_df, prev_num


def _find_opt_CONST(df): 

    real = df.real 
    yhat = df.yhat

    adj = 0.005 
    const = .1
    minimum, ret = -1, 1 
    while const < 2.5: 
        diff = (yhat*const) - real 
        diff = sum(abs(diff)) 
        if minimum == -1: 
            minimum = diff 
            ret = const 
        elif diff < minimum: 
            minimum = diff 
            ret = const 
        const += adj 
        
    return ret 


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
    
    result['real'] = val_data
    
    for col in col_list[1:]: result[col] = round(result[col] - prev_num, 0)

    if ADJ_CONST == -1: 
        ADJ_CONST = _find_opt_CONST(result) 

    for col in col_list[1:]: result[col] = round(result[col]*ADJ_CONST, 0)

    tmp = [val_data[0]] 
    for i in range(1, len(val_data)): 
        tmp.append(val_data[i] - val_data[i-1])
    val_data = tmp 
    result['real'] = val_data


    result['lower_ratio'] = result.yhat_lower / result.yhat 
    result['upper_ratio'] = result.yhat_upper / result.yhat 


    adj_yhat = [result.iloc[0].yhat]
    lower, upper = [result.iloc[0].yhat_lower*1.1], [result.iloc[0].yhat_upper*0.9]
    for i in range(1, len(result)): 
        prev, cur = result.iloc[i-1], result.iloc[i] 
        diff = cur.yhat-prev.yhat
        adj_yhat.append(diff)
        lower.append(diff * cur.lower_ratio)
        upper.append(diff * cur.upper_ratio)
        
    result['yhat'] = adj_yhat 
    result['yhat_lower'] = lower 
    result['yhat_upper'] = upper 

    result.drop(['lower_ratio', 'upper_ratio'], axis=1, inplace=True)
    return result, ADJ_CONST

def upsert_inference_data(ADJ_CONST): 

    pred_df, prev_num = predict_FBProphet_model(ADJ_CONST)
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
        val_df, ADJ_CONST = validate_FBProphet_model(ADJ_CONST) 

        conn = conn_db() 

        validate_FBProphet_collection = conn.DomesticCOVID.validate_FBProphet 
        validate_FBProphet_collection.drop()

        col_list = val_df.columns 
        doc_list = list() 

        insert_data(val_df, validate_FBProphet_collection, check=False)

        conn.close() 
        return True, ADJ_CONST 

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
    res, ADJ_CONST = insert_validate_FBProphet_data(ADJ_CONST=-1)
    print("validate FBPropeht data Insert: ", res)
    ADJ_CONST = 1.
    print("predict FBProphet data Upsert: ", upsert_inference_data(ADJ_CONST))
     