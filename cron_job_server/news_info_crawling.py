from bs4 import BeautifulSoup
from datetime import datetime
from newspaper import Article
from selenium import webdriver 

import requests
import re 

from TextRank import TextRank 


# 1. Naver News API call && crawling contents 
URL = "https://openapi.naver.com/v1/search/news.json" 
CLIENT_ID = "3ASKoK9e70DQQ_upgqfp"
CLIENT_SECRET = "2Ht5jnkPxK"


def check_datetime_str(astring): 
    astring = astring.split()[0]
    time_format = '%Y.%m.%d.'
    try: 
        datetime.strptime(astring, time_format) 
        return True 
    except ValueError: return False 

def crawling_each_news(url, doc): 
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' }
    
    
    try: 
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select_one('h3[id=articleTitle]').text
        doc['title'] = title 
        
        press = soup.select_one('div[class=press_logo] > a > img')
        doc['press'] = press['alt']

        date_candidates = soup.select('div[class=sponsor] > span')
        for date_candidate in date_candidates: 
            date_candidate = date_candidate.text
            if check_datetime_str(date_candidate): 
                doc['date'] = date_candidate
                break 
        if doc['date'][-5] == ' ': doc['date'] = doc['date'][:-4] + '0' + doc['date'][-4:]
        contents = Article(url, language='ko')
        contents.download() 
        contents.parse() 
        doc['content'] = contents.text

        try:
            image_url = soup.select("span.end_photo_org > img")[0].get('src')
        except: image_url = '' #이미지 없는 경우

        doc['img_url'] = image_url
        return doc 

    except: 
        # print(url, "Entertain or Sport news... Or not Naver News")
        return 


def get_news_api(query, num=100, sort_way='sim'): 

    headers = { 
        'X-Naver-Client-Id': CLIENT_ID, 
        'X-Naver-Client-Secret': CLIENT_SECRET
    }

    params = { 
        'query': query, 
        'display': num, 
        'sort': sort_way
    }

    res = requests.get(URL, headers=headers, params=params)
    res = res.json()['items']
    
    doc_list = list() 
    for elem in res: 
        url = elem.get('link', '')
        if not url: continue 
        doc = {'url': url} 
        
        crawling_res = crawling_each_news(url, doc) 
        if crawling_res: doc_list.append(crawling_res)

    return doc_list 


# 2. 코로나바이러스감염증-19 최근 게시된 공지사항 크롤링
def briefing_crawing():
    url = 'http://ncov.mohw.go.kr/tcmBoardList.do?brdId=&brdGubun=&dataGubun=&ncvContSeq=&contSeq=&board_id=140&gubun='

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    browser = webdriver.Chrome('./chromedriver', chrome_options=options) # 같은 디렉토리 내에 chtromdriver.exe
    browser.implicitly_wait(1)

    browser.get(f'{url}')
    browser.implicitly_wait(1)
    title = browser.find_element_by_css_selector("""#content > div > div.board_list > table > tbody > tr:nth-child(1) > td.ta_l > a""").text.strip() 
    date = browser.find_element_by_css_selector("""#content > div > div.board_list > table > tbody > tr:nth-child(1) > td:nth-child(4)""").text.strip() 

    browser.find_element_by_css_selector("""#content > div > div.board_list > table > tbody > tr:nth-child(1) > td.ta_l > a""").click()
    texts = browser.find_element_by_css_selector("""#content > div > div.board_view > div.bv_content""").text
    browser.close()
    
    texts = re.sub('[□○※【】]', '', texts)
    texts = texts.replace('▲', '')
    texts = texts.replace('▸', ', ')
    
    textrank = TextRank(texts)
    results =  textrank.summarize(3)

    doc = dict( 
        contents=results, 
        title=title, 
        date=date 
    )

    return doc
    