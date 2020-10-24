
from flask import Flask, jsonify
from flask_cors import CORS
import os 
import json

from functions.conn_mongodb import get_dashboard_data, get_news_data
from functions.sample_plot import get_plot_sample1, get_plot_sample2

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app)
# CORS enabled so react frontend can pull data from python backend

@app.route('/api/test')
def hello_world():
    return 'Hello, World!'

@app.route('/api/plot2')
def plot2():
    return get_plot_sample2()


@app.route('/api/plot1')
def plot1():
    return get_plot_sample1() 
    

@app.route('/api/dashboard')
def dashboard(): 
    res = get_dashboard_data()
    return json.dumps(res)

@app.route('/api/news-data')
def news_data(): 
    # res = get_news_data() 
    # return json.dumps(res) 
    return json.dumps(get_news_data())

# Flask Main Setting -> running app ========================


@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, 
                    port=os.environ.get('PORT', 5000))
# ==========================================================