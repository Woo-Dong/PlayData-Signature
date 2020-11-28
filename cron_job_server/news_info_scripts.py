from bson.objectid import ObjectId
from datetime import datetime
import sys 


from news_info_crawling import get_news_api, briefing_crawing
from Clustering import news_cluster 
from functions import conn_db


def insert_news_data(doc_list, collection, *chk_keys, check=False): 
    
    insert_docs = list() 
    for doc in doc_list: 
    
        # Check if duplicated
        if check: 
            query_dict = {k: doc[k] for k in chk_keys}
            if collection.find_one(query_dict): continue

        insert_docs.append(doc)

    if insert_docs: 
        collection.insert_many(insert_docs)
        print(len(insert_docs), "docs added")
        return True 

    return False 

def insert_brefing_data(doc, collection, reset=True): 
    
    if reset: collection.drop() 
    collection.insert(doc) 
    return True 

# python news_API.py 코로나 200 100 
# 200개 뉴스 수집 및 수집된 뉴스 100개만 유지 
if __name__ == '__main__': 
    
    # 1. Crawling and insert news data 
    # query = sys.argv[1] if len(sys.argv) > 1 else None 
    # if not query: print("Error occuered! => failed to get query word"); exit() 

    # news_query_num = sys.argv[2] if len(sys.argv) > 2 else 100
    conn = conn_db() 
    raw_news_collection = conn.NewsData.raw_news
    
    query_list = '''코로나19
        바이러스
        감염증
        방역
        확진자
        확산
        접촉
        증상
        마스크
        격리
        거리두기'''

    query_list = [elem.strip() for elem in query_list.split('\n')]
    news_query_num = 10
    for query in query_list: 
        result = get_news_api(query, int(news_query_num))
        print("Insert news data: ", query, insert_news_data(result, raw_news_collection, 'title', check=True))

    # chk_limit = sys.argv[3] if len(sys.argv) > 3 else None 
    chk_limit = 300
    if chk_limit: 
        limit_num = int(chk_limit) 

        id_list = list() 

        for idx, doc in enumerate(raw_news_collection.find({})): 
            id_list.append((str(doc['_id']), doc['date']))

        delete_num = idx - limit_num 

        if delete_num > 0: 
            id_list.sort(key=lambda x:x[1])
            for _id, _ in id_list[:delete_num]: 
                raw_news_collection.remove({'_id': ObjectId(_id) })

            cnt = 0 
            for elem in raw_news_collection.find({}): cnt += 1 
            print("remove doc_num: ", cnt) 


    # 1-2. News Clustering Part 
    
    article_data = [elem['content'] for elem in raw_news_collection.find({})]
    results = news_cluster(article_data, sent_n=3, n_clusters=5)

    cluster_summary_collection = conn.NewsData.cluster_summary 
    cluster_summary_collection.drop() 
    docs = list() 
    for res in results: 
        doc = dict( 
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            content=res
        )
        docs.append(doc) 
    cluster_summary_collection.insert_many(docs) 
    print("Insert cluster_summary data: ", True)


    # 2. brefing info Part 
    brefing_info_collection = conn.NewsData.brefing_info 
    doc = briefing_crawing() 
    print("Insert brefing_info data: ", insert_brefing_data(doc, brefing_info_collection, reset=True))
    
    
    conn.close() 