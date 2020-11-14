from datetime import datetime 
import pandas as pd 
import requests 
import io

from functions import conn_db, insert_data 


def crawling_global_covid(): 
    url_confirmed = 'https://tradingeconomics.com/country-list/coronavirus-cases?continent=g20'
    url_deaths = 'https://tradingeconomics.com/country-list/coronavirus-deaths?continent=g20'
    url_recovered = 'https://tradingeconomics.com/country-list/coronavirus-recovered?continent=g20'

    raw_df = list()

    # Crawling Data From Web
    for elem in [url_confirmed, url_deaths, url_recovered]: 
        raw_df.append(pd.read_html(elem)[0]) 
    country = raw_df[0].Country

    # Setting DataFrame
    col_list = ['date', 'country', 'confirmed', 'deaths', 'recovered']
    global_cumul_df = pd.DataFrame(columns=col_list)
    global_cumul_df['country'] = country
    global_cumul_df['date'] = datetime.today().strftime("%Y-%m-%d")

    global_daily_df = global_cumul_df.copy() 

    for col, df in zip(col_list[2:], raw_df): 
        global_cumul_df[col] = df['Last']
        global_daily_df[col] = df['Last'] - df['Previous']

    # Insert data - MongoDB, database name: 'GlobalCOVID' 
    conn = conn_db() 

    global_daily_collection = conn.GlobalCOVID.daily 
    global_cumul_collection = conn.GlobalCOVID.cumul 

    print(datetime.now())
    print("crawling_global_covid cumul Updated: ", insert_data(global_cumul_df, global_cumul_collection, 'date', 'country'))
    print("crawling_global_covid daily Updated: ", insert_data(global_daily_df, global_daily_collection, 'date', 'country'))
    conn.close() 


def get_domestic_covid_cumul(): 

    conn = conn_db() 
    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul 

    kr_daily_csv_link = "https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_daily.csv"
    csv_content = requests.get(kr_daily_csv_link).content
    domestic_cumul_df = pd.read_csv(io.StringIO(csv_content.decode('utf-8'))) 
    domestic_cumul_df.date = pd.to_datetime(domestic_cumul_df.date, format='%Y%m%d')
    domestic_cumul_df.date = domestic_cumul_df.date.apply(lambda x: x.strftime("%Y-%m-%d"))

    print("get_domestic_covid_cumul Updated: ", insert_data(domestic_cumul_df, domestic_cumul_collection, 'date'))

    conn.close() 


# TODO
def get_news_API(): 
    return 


# Main Function  
if __name__ == "__main__":
    crawling_global_covid()
    get_domestic_covid_cumul() 
    # find_data()