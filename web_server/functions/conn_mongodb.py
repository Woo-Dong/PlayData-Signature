from pymongo import MongoClient


MONGO_URI = "mongodb://{dbuser}:{dbpassword}@ds253918.mlab.com:53918/signature"
MONGO_URI = MONGO_URI.format(dbuser='admin', dbpassword='user123')

conn = MongoClient(MONGO_URI, retryWrites="false")
db = conn.get_default_database()

sample_db = db['sample']

def get_dashboard_data(): 
    result = sample_db.find().sort("date", -1).limit(2)
    today, yesterday = list(result)

    col_list = ['confirmed', 'released', 'death']
    today_col = 'today_'
    res_dict = dict() 
    for elem in col_list: 
        new_colname = today_col + elem
        res_dict[new_colname] = today[elem] - yesterday[elem] 
        res_dict[elem] = today[elem]
    res_dict['date'] = today['date']
    return res_dict