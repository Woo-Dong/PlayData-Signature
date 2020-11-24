from pymongo import MongoClient
from datetime import datetime
import pandas as pd 
import requests
import io
import os

from functions import conn_db, insert_data

def covid19_kor_insert(file_name):
    #데이터 불러오기
    df = pd.read_csv(file_name, encoding='ANSI') # 01.31 - 2020.10.31 까지의 데이터
    
    #인덱스
    df = df.reset_index()
    
    #불필요 컬럼 제거
    df.drop(['구분별', '상태별', '항목', '단위'], axis=1, inplace=True)
    
    #행렬 변경
    df = df.transpose()
    
    df = df.drop(df.index[0])
    df = df.drop(df.index[275])
    
    #컬럼 rename
    df = df.rename({0:'overseas', 1:'domestic', 2:'confirmed_n', 3:'confirmed_c', 4:'iso_n', 5:'iso_c', 6:'iso_rel_n', 7:'iso_rel_c', 8:'death_n', 9:'death_c',
                 10:'m_confirmed_n', 11:'m_confirmed_c', 12:'m_death_n', 13:'m_death_c', 14:'f_confirmed_n', 15:'f_confirmed_c', 16:'f_death_n', 17:'f_death_c',
                 18:'00s_confirmed_n', 19:'00s_confirmed_c', 20:'00s_death_n',21:'00s_death_c',
                 22:'10s_confirmed_n', 23:'10s_confirmed_c', 24:'10s_death_n',25:'10s_death_c',
                 26:'20s_confirmed_n', 27:'20s_confirmed_c', 28:'20s_death_n',29:'20s_death_c',
                 30:'30s_confirmed_n', 31:'30s_confirmed_c', 32:'30s_death_n',33:'30s_death_c',
                 34:'40s_confirmed_n', 35:'40s_confirmed_c', 36:'40s_death_n',37:'40s_death_c',
                 38:'50s_confirmed_n', 39:'50s_confirmed_c', 40:'50s_death_n',41:'50s_death_c',
                 42:'60s_confirmed_n', 43:'60s_confirmed_c', 44:'60s_death_n',45:'60s_death_c',
                 46:'70s_confirmed_n', 47:'70s_confirmed_c', 48:'70s_death_n',49:'70s_death_c',
                 50:'80s_confirmed_n', 51:'80s_confirmed_c', 52:'80s_death_n',53:'80s_death_c',
                 54:'seoul_overseas', 55:'seoul_domestic', 56:'seoul_confirmed_n',57:'seoul_confirmed_c',58:'seoul_iso_n',59:'seoul_iso_c',60:'seoul_iso_rel_n',61:'seoul_iso_rel_c',62:'seoul_death_n',63:'seoul_death_c',
                 64:'bs_overseas', 65:'bs_domestic', 66:'bs_confirmed_n',67:'bs_confirmed_c',68:'bs_iso_n',69:'bs_iso_c',70:'bs_iso_rel_n',71:'bs_iso_rel_c',72:'bs_death_n',73:'bs_death_c',
                 74:'tk_overseas', 75:'tk_domestic', 76:'tk_confirmed_n',77:'tk_confirmed_c',78:'tk_iso_n',79:'tk_iso_c',80:'tk_iso_rel_n',81:'tk_iso_rel_c',82:'tk_death_n',83:'tk_death_c',
                 84:'ic_overseas', 85:'ic_domestic', 86:'ic_confirmed_n',87:'ic_confirmed_c',88:'ic_iso_n',89:'ic_iso_c',90:'ic_iso_rel_n',91:'ic_iso_rel_c',92:'ic_death_n',93:'ic_death_c',
                 94:'kj_overseas', 95:'kj_domestic', 96:'kj_confirmed_n',97:'kj_confirmed_c',98:'kj_iso_n',99:'kj_iso_c',100:'kj_iso_rel_n',101:'kj_iso_rel_c',102:'kj_death_n',103:'kj_death_c',
                 104:'dj_overseas', 105:'dj_domestic', 106:'dj_confirmed_n',107:'dj_confirmed_c',108:'dj_iso_n',109:'dj_iso_c',110:'dj_iso_rel_n',111:'dj_iso_rel_c',112:'dj_death_n',113:'dj_death_c',
                 114:'ulsan_overseas', 115:'ulsan_domestic', 116:'ulsan_confirmed_n',117:'ulsan_confirmed_c',118:'ulsan_iso_n',119:'ulsan_iso_c',120:'ulsan_iso_rel_n',121:'ulsan_iso_rel_c',122:'ulsan_death_n',123:'ulsan_death_c',
                 124:'sj_overseas', 125:'sj_domestic', 126:'sj_confirmed_n',127:'sj_confirmed_c',128:'sj_iso_n',129:'sj_iso_c',130:'sj_iso_rel_n',131:'sj_iso_rel_c',132:'sj_death_n',133:'sj_death_c',
                 134:'gg_overseas', 135:'gg_domestic', 136:'gg_confirmed_n',137:'gg_confirmed_c',138:'gg_iso_n',139:'gg_iso_c',140:'gg_iso_rel_n',141:'gg_iso_rel_c',142:'gg_death_n',143:'gg_death_c',
                 144:'kw_overseas', 145:'kw_domestic', 146:'kw_confirmed_n',147:'kw_confirmed_c',148:'kw_iso_n',149:'kw_iso_c',150:'kw_iso_rel_n',151:'kw_iso_rel_c',152:'kw_death_n',153:'kw_death_c',
                 154:'cb_overseas', 155:'cb_domestic', 156:'cb_confirmed_n',157:'cb_confirmed_c',158:'cb_iso_n',159:'cb_iso_c',160:'cb_iso_rel_n',161:'cb_iso_rel_c',162:'cb_death_n',163:'cb_death_c',
                 164:'cn_overseas', 165:'cn_domestic', 166:'cn_confirmed_n',167:'cn_confirmed_c',168:'cn_iso_n',169:'cn_iso_c',170:'cn_iso_rel_n',171:'cn_iso_rel_c',172:'cn_death_n',173:'cn_death_c',
                 174:'jb_overseas', 175:'jb_domestic', 176:'jb_confirmed_n',177:'jb_confirmed_c',178:'jb_iso_n',179:'jb_iso_c',180:'jb_iso_rel_n',181:'jb_iso_rel_c',182:'jb_death_n',183:'jb_death_c',
                 184:'jn_overseas', 185:'jn_domestic', 186:'jn_confirmed_n',187:'jn_confirmed_c',188:'jn_iso_n',189:'jn_iso_c',190:'jn_iso_rel_n',191:'jn_iso_rel_c',192:'jn_death_n',193:'jn_death_c',
                 194:'kb_overseas', 195:'kb_domestic', 196:'kb_confirmed_n',197:'kb_confirmed_c',198:'kb_iso_n',199:'kb_iso_c',200:'kb_iso_rel_n',201:'kb_iso_rel_c',202:'kb_death_n',203:'kb_death_c',
                 204:'kn_overseas', 205:'kn_domestic', 206:'kn_confirmed_n',207:'kn_confirmed_c',208:'kn_iso_n',209:'kn_iso_c',210:'kn_iso_rel_n',211:'kn_iso_rel_c',212:'kn_death_n',213:'kn_death_c',
                 214:'jj_overseas', 215:'jj_domestic', 216:'jj_confirmed_n',217:'jj_confirmed_c',218:'jj_iso_n',219:'jj_iso_c',220:'jj_iso_rel_n',221:'jj_iso_rel_c',222:'jj_death_n',223:'jj_death_c',
                 224:'qs_overseas', 225:'qs_domestic', 226:'qs_confirmed_n',227:'qs_confirmed_c',228:'qs_iso_n',229:'qs_iso_c',230:'qs_iso_rel_n',231:'qs_iso_rel_c',232:'qs_death_n',233:'qs_death_c',
               }, axis='columns')
    
    adict = {
        "seoul": "서울", "bs": "부산", "tk": "대구", 
        "ic": "인천", "kj": "광주", "dj": "대전", "ulsan": "울산", 
        "sj": "세종", "gg": "경기", "kw": "강원", "cb": "충북", "cn": "충남", "jb": "전북",
        "jn": "전남", "kb": "경북", "kn": "경남", "jj": "제주", "qs": "검역",
        "00s": "0-9세", "10s": "10-19세", "20s": "20-29세", "30s": "30-39세",
        "40s": "40-49세", "50s": "50-59세", "60s": "60-69세",
        "70s": "70-79세", "80s": "80세 이상",
        "m": "남성", "f": "여성"    
    }

    #null값 처리
    df = df.fillna(0)
    
    #index reset
    df = df.reset_index()
    
    df = df.rename({'index':'date'}, axis='columns')
    df.set_index('date', inplace=True)
    
    ##area, age, gender 별로 데이터 concat
    #go: area 데이터 추출함수
    def extract_area(column): 
        col_list = [elem for elem in df.columns if column in elem and '_n' in elem] 

        adj_col_list = [elem.split('_')[1] for elem in col_list]
        adj_col_list[2] += '_rel'

        ret_df = df[col_list]
        ret_df = ret_df.reset_index()
        ret_df['area'] = adict[column]

        ret_df.rename({k: v for k, v in zip(col_list, adj_col_list)}, axis=1, inplace=True)
        return ret_df
    
    covid19_area = pd.concat([extract_area('seoul'), extract_area('bs'), extract_area('tk'), extract_area('ic'), extract_area('kj'), extract_area('dj'), extract_area('ulsan'), extract_area('sj'), extract_area('gg'),
          extract_area('kw'), extract_area('cb'), extract_area('cn'), extract_area('jb'), extract_area('jn'), extract_area('kb'), extract_area('kn'), extract_area('jj'), extract_area('qs')])

    covid19_area = covid19_area[['date','area','confirmed','iso','iso_rel','death']]
    covid19_area['date'] = covid19_area['date'].str.replace('. ', '-')
    covid19_area.rename({'iso': 'isolated', 'iso_rel': 'released'}, axis=1, inplace=True) 
    covid19_area = covid19_area[covid19_area['date'] != 'Unnamed-302']
    print(covid19_area)

    #gender 데이터 추출
    df_m = df[['m_confirmed_n', 'm_death_n']]
    df_m = df_m.rename({'m_confirmed_n':'confirmed', 'm_death_n':'death'}, axis='columns')
    df_m['gender'] = adict['m']
    df_f = df[['f_confirmed_n', 'f_death_n']]
    df_f = df_f.rename({'f_confirmed_n':'confirmed', 'f_death_n':'death'}, axis='columns')
    df_f['gender'] = adict['f']

    covid19_gender = pd.concat([df_m, df_f])
    covid19_gender = covid19_gender.reset_index()
    covid19_gender = covid19_gender[['date', 'gender', 'confirmed', 'death']]
    covid19_gender['date'] = covid19_gender['date'].str.replace('. ', '-')
    covid19_gender = covid19_gender[covid19_gender['date']!='Unnamed-302']
    print(covid19_gender)
    
    #go: age 데이터 추출함수
    def extract_age(column): 
        col_list = [elem for elem in df.columns if column in elem and '_n' in elem] 

        adj_col_list = [elem.split('_')[1] for elem in col_list]

        ret_df = df[col_list]
        ret_df = ret_df.reset_index()
        ret_df['age'] = adict[column]

        ret_df.rename({k: v for k, v in zip(col_list, adj_col_list)}, axis=1, inplace=True)
        return ret_df
    
    covid19_age = pd.concat([extract_age('00s'), extract_age('10s'), extract_age('20s'), extract_age('30s'), extract_age('40s'), extract_age('50s'),
                          extract_age('60s'), extract_age('70s'), extract_age('80s')])
    covid19_age = covid19_age[['date', 'age', 'confirmed', 'death']]
    covid19_age['date'] = covid19_age['date'].str.replace('. ', '-')
    covid19_age = covid19_age[covid19_age['date'] != 'Unnamed-302']
    print(covid19_age)

    # mongodb에 데이터 insert
    conn = conn_db() 

    kor_area_collection = conn.DomesticDetailedCOVID.area
    kor_gender_collection = conn.DomesticDetailedCOVID.gender
    kor_age_collection = conn.DomesticDetailedCOVID.age

    print("crawling_covid19_area Updated: ", insert_data(covid19_area, kor_area_collection, 'date', 'area'))
    print("crawling_covid19_gender Updated: ", insert_data(covid19_gender, kor_gender_collection, 'date', 'gender'))
    print("crawling_covid19_age Updated: ", insert_data(covid19_age, kor_age_collection, 'date', 'age'))
    conn.close()

if __name__ == "__main__":
    covid19_kor_insert('data_1123.csv')