from datetime import datetime 
import pandas as pd 
import requests 
import io

from crawling_part import crawling_global_covid, crawling_domestic_covid_cumul, crawling_domestic_detailed_covid
from functions import conn_db, insert_data, upsert_data


def insert_global_covid(): 
     
    global_daily_df, global_cumul_df = crawling_global_covid() 

    # Insert data - MongoDB, database name: 'GlobalCOVID' 
    conn = conn_db() 

    global_daily_collection = conn.GlobalCOVID.daily 
    global_cumul_collection = conn.GlobalCOVID.cumul 

    print(datetime.now())
    print("insert_global_covid daily Updated: ", insert_data(global_daily_df, global_daily_collection, 'date', 'country'))
    print("insert_global_covid cumul Updated: ", insert_data(global_cumul_df, global_cumul_collection, 'date', 'country'))
    conn.close() 

    return True 


def insert_domestic_covid_cumul(): 

    domestic_cumul_df = crawling_domestic_covid_cumul() 

    conn = conn_db() 
    domestic_cumul_collection = conn.DomesticCOVID.domestic_cumul 

    print("insert_domestic_covid_cumul Updated: ", insert_data(domestic_cumul_df, domestic_cumul_collection, 'date'))
    conn.close() 

    return True 


def insert_domestic_detailed_covid(): 

    (area_df, gender_df, age_df), cum_df = crawling_domestic_detailed_covid()

    conn = conn_db() 
    domestic_detailed_area_collection = conn.DomesticDetailedCOVID.area
    domestic_detailed_gender_collection = conn.DomesticDetailedCOVID.gender
    domestic_detailed_age_collection = conn.DomesticDetailedCOVID.age

    print("insert_domestic_detailed_covid - area: ", 
            upsert_data(area_df, domestic_detailed_area_collection, ['date', 'area']))
    
    print("insert_domestic_detailed_covid - gender: ", 
            upsert_data(gender_df, domestic_detailed_gender_collection, ['date', 'gender'])) 

    print("insert_domestic_detailed_covid - age: ", 
            upsert_data(age_df, domestic_detailed_age_collection, ['date', 'age']))


    domestic_detailed_cumul_collection = conn.DomesticDetailedCOVID.cumul 

    print("insert_domestic_detailed_covid - cumul: ", 
            upsert_data(cum_df, domestic_detailed_cumul_collection, ['type', 'attr']))

    conn.close() 

    return True 



# TODO
def get_news_API(): 
    pass 


# Main Function  
if __name__ == "__main__":
    insert_global_covid()
    insert_domestic_covid_cumul()
    insert_domestic_detailed_covid()