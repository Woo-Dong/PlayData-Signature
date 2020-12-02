from selenium import webdriver 
from datetime import datetime 
import requests 
import pandas as pd 
import numpy as np 
import io 



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

    return global_daily_df, global_cumul_df 

def crawling_domestic_covid_cumul(): 
    kr_daily_csv_link = "https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_daily.csv"
    csv_content = requests.get(kr_daily_csv_link).content

    domestic_cumul_df = pd.read_csv(io.StringIO(csv_content.decode('utf-8'))) 
    domestic_cumul_df.date = pd.to_datetime(domestic_cumul_df.date, format='%Y%m%d')
    domestic_cumul_df.date = domestic_cumul_df.date.apply(lambda x: x.strftime("%Y-%m-%d"))

    return domestic_cumul_df

# (area_df, gender_df, age_df), cum_df = crawling_domestic_detailed_covid()
def crawling_domestic_detailed_covid(): 

    url = 'https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_COVID19_005_D'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # Crhomedriver 프로그램 필요 
    browser = webdriver.Chrome('./chromedriver', chrome_options=options) 
    browser.implicitly_wait(1.)

    browser.get(f'{url}')
    browser.implicitly_wait(2.5)

    date = browser.find_element_by_css_selector('#mainTableT > thead > tr:nth-child(1) > th:nth-child(3)')
    date = date.text.strip().replace('. ', '-')

    res = browser.find_element_by_css_selector('#mainTable > tbody')


    text_list = [elem.strip() for elem in res.text.strip().split('\n')] 

    n = len(text_list)
    result = list() 


    result.append(text_list[:32][1:12] )

    idx = 32
    for i in range(1, 19): 
        if i == 1: 
            result.append( text_list[idx:idx+32][1:12] )
            idx += 32
        else: 
            result.append( text_list[idx:idx+31][:11]  )
            idx += 31

    col_list= ['area','overseas','domestic','confirmed','confirmed_cumul','isolated','isolated_cumul','released','released_cumul','death','death_cumul']
    daily_area_df = pd.DataFrame(result, columns=col_list)
    daily_area_df['date'] = date 
    daily_area_df = daily_area_df.replace('-', np.nan)
    daily_area_df = daily_area_df.fillna(0) 

    # print(daily_area_df) 
    
    # daily_area_new = daily_area_df[['area', 'overseas', 'domestic','confirmed', 'isolated','released','death']]
    daily_area_new = daily_area_df[['date', 'area', 'confirmed', 'isolated','released','death']]
    daily_area_new = daily_area_new[daily_area_new['area'] != '소계']

    daily_area_cum = daily_area_df[['area', 'confirmed_cumul', 'isolated_cumul','released_cumul','death_cumul']]
    daily_area_cum = daily_area_cum.rename({'area':'attr'}, axis='columns')
    daily_area_cum['type'] = 'area'

    n = len(text_list)
    result = list() 
    result.append(text_list[591:][1:12] )

    idx = 591
    for i in range(1, 3):
        if i == 1:
            idx += 32
        else:
            result.append(text_list[idx:idx+31][:11])
            idx += 31

    col_list= ['gender','overseas','domestic','confirmed','confirmed_cumul','isolated','isolated_cumul','released','released_cumul','death','death_cumul']
    daily_gender_df = pd.DataFrame(result, columns=col_list)
    daily_gender_df['date'] = date
    daily_gender_df = daily_gender_df.replace('-', np.nan)
    daily_gender_df = daily_gender_df.fillna(0) 
    
    # daily_gender_new = daily_gender_df[['gender', 'overseas', 'domestic','confirmed', 'isolated','released','death']]
    daily_gender_new = daily_gender_df[['date', 'gender', 'confirmed', 'death']]
    


    daily_gender_cum = daily_gender_df[['gender', 'confirmed_cumul', 'isolated_cumul','released_cumul','death_cumul']]
    daily_gender_cum = daily_gender_cum.rename({'gender':'attr'}, axis='columns')
    daily_gender_cum['type'] = 'gender'


    n = len(text_list)
    result = list() 
    result.append(text_list[654:][1:12] )

    idx = 654
    for i in range(1, 10): 
        if i == 1: 
            idx += 32
        else: 
            result.append( text_list[idx:idx+31][:11]  )
            idx += 31

        
    col_list= ['age','overseas','domestic','confirmed','confirmed_cumul','isolated','isolated_cumul','released','released_cumul','death','death_cumul']

    daily_age_df = pd.DataFrame(result, columns=col_list)
    daily_age_df['date'] = date
    daily_age_df = daily_age_df.replace('-', np.nan)
    daily_age_df = daily_age_df.fillna(0) 

    # daily_age_new = daily_age_df[['age', 'overseas', 'domestic','confirmed', 'isolated','released','death']]
    daily_age_new = daily_age_df[['date', 'age', 'confirmed', 'death']]

    daily_age_cum = daily_age_df[['age', 'confirmed_cumul', 'isolated_cumul','released_cumul','death_cumul']]
    daily_age_cum = daily_age_cum.rename({'age':'attr'}, axis='columns')
    daily_age_cum['type'] = 'age'
    
    
    df_cum = pd.concat([daily_area_cum, daily_gender_cum])
    df_cum = pd.concat([df_cum, daily_age_cum])
    df_cum = df_cum[['type', 'attr', 'confirmed_cumul', 'isolated_cumul','released_cumul','death_cumul']]
    df_cum = df_cum.rename({'confirmed_cumul':'confirmed','isolated_cumul':'isolated','released_cumul':'released','death_cumul':'death'}, axis='columns')

    return (daily_area_new, daily_gender_new, daily_age_new), df_cum  