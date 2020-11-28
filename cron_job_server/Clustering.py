from pymongo import MongoClient
import pandas as pd
import re
from random import *

#text
from nltk.tokenize import sent_tokenize
from konlpy.tag import Kkma, Mecab 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import pandas as pd

#cluster
from sklearn.cluster import KMeans

from TextRank import TextRank 

#wordcloud
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS


def re_preprocessing(sentence):
    sentence = re.sub('[^0-9가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z%ℓ.,]', ' ', sentence)
    return sentence


def news_cluster(article_data, sent_n, n_clusters=5):
    contents= [sent_tokenize(x) for x in article_data]
    
    # 뉴스데이터 전처리
    contents_list = list()
    stop_words = ['머니S', '머니투데이', '구독', '파이낸셜뉴스', '헬스조선', '중앙일보', '프레시안', '조선일보', '.com',
                 '매일경제', '한국', '엠빅', '뉴시스', '무단전재재', '오마이뉴스', '연합뉴스', '연합뉴스TV', 'JTBC','SBS',
                  'MBC','KBS','한겨레','YTN','MBN','TV조선','채널A','동아일보','뉴스1', '강원일보','경향신문','세계일보',
                  '한국일보','서울신문','노컷뉴스','이데일리']
    
    for content in contents:
        new_str = ''
        for sent in content:
            has_stopword = False
            for word in stop_words:
                if word in sent:
                    has_stopword = True
                    break
            if has_stopword:
                continue
            else:
                new_str += sent +' '

        contents_list.append(new_str)
        
    df = pd.DataFrame(contents_list)

    df['content_cleaned'] = df[0].apply(re_preprocessing)
    content = df['content_cleaned'].tolist()
    
    # clustering
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(content)
    X = normalize(X)

    kmeans = KMeans(n_clusters=n_clusters).fit(X)

    labels = kmeans.labels_
    # centers = kmeans.cluster_centers_

    df['labels'] = labels
    
    clustered_sentences = list() 
    for clust_idx in df.labels.unique(): 
        sentences = df[df['labels'] == clust_idx].content_cleaned 
        clustered_sentences.append(' '.join([sent for sent in sentences]))

    # str_list = str(clustered_sentences)
    # nlpy = Mecab(dicpath='C:/mecab/mecab-ko-dic')
    # nouns = nlpy.nouns(str_list)
    # str_list= str(nouns)
    # str_list = str_list.replace("'",'')

    # wordcloud = WordCloud(font_path='NanumGothic.ttf', background_color='white', max_words=50).generate(str_list)
    # plt.figure(figsize=(11,11))
    # plt.imshow(wordcloud, interpolation='None')
    # plt.axis('off')
    # plt.show() 

    return ['\n'.join(TextRank(news).summarize(sent_n)) for news in clustered_sentences]