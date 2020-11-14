
from pymongo import MongoClient
from datetime import datetime 
import pandas as pd 

def conn_db(collection): 
    MONGO_URI = "mongodb://{dbuser}:{dbpassword}@ds253918.mlab.com:53918/signature"
    MONGO_URI = MONGO_URI.format(dbuser='admin', dbpassword='user123')

    conn = MongoClient(MONGO_URI, retryWrites="false")
    db = conn.get_default_database()
    ret_db = db[collection]

    return ret_db

def crawling_global_covid_data(): 

    try: 

        url_confirmed = 'https://tradingeconomics.com/country-list/coronavirus-cases?continent=g20'
        url_deaths = 'https://tradingeconomics.com/country-list/coronavirus-deaths?continent=g20'
        url_recovered = 'https://tradingeconomics.com/country-list/coronavirus-recovered?continent=g20'

        raw_df = list()

        # Crawling Data From Web
        for elem in [url_confirmed, url_deaths, url_recovered]: 
            raw_df.append(pd.read_html(elem)[0]) 
        country = raw_df[0].Country


        # Setting DataFrame
        col_list = ['date', 'country', 'Confirmed', 'Deaths', 'Recovered']
        global_df = pd.DataFrame(columns=col_list)

        global_df['country'] = country
        global_df['date'] = datetime.today().strftime("%Y-%m-%d")

        # append rows to DataFrame - row(country, date, Confirmed, Deaths, Recovered, 
        #                              Confirmed_daily, Deaths_daily, Recovered_daily)
        for col, df in zip(col_list[2:], raw_df): 
            global_df[col] = df['Last']
            global_df[col + '_daily'] = df['Last'] - df['Previous']


        # Insert data - MongoDB, database name: 'global' 
        global_db = conn_db('global')

        doc_list = list() 
        for _, row in global_df.iterrows(): 
        
            # Check if duplicated
            if global_db.find({'date': row['date'], 'country': row['country']}): continue

            doc = {col: val for col, val in zip(global_df.columns, row)} 
            doc_list.append(doc)

        if doc_list: global_db.insert_many(doc_list)
        return True

    except: 
        print("Error Ocurred => crawling_global_covid_data Func")
        return False 
