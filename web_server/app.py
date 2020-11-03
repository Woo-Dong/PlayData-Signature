
from sanic import Sanic 
from sanic.response import json_dumps, file, json
from sanic_cors import CORS 
import os 

from functions.conn_mongodb import get_dashboard_data, get_news_data
from functions.sample_plot import get_plot_sample1, get_plot_sample2

# app = Sanic(__name__, static_folder='build', static_url_path='')
app = Sanic(__name__)
app.static('', 'build')
CORS(app)
# CORS enabled so react frontend can pull data from python backend


@app.route('/api/test')
def hello_world(request):
    return 'Hello, World!'

@app.route('/api/plot2')
async def plot2(request):
    return json(get_plot_sample2())

@app.route('/api/plot1')
async def plot1(request):
    return json(get_plot_sample1())
    

@app.route('/api/dashboard')
async def dashboard(request): 
    res = get_dashboard_data()
    return json(res)

@app.route('/api/news-data')
async def news_data(request): 
    return json(get_news_data())

# Sanic Main Setting -> running app ========================
@app.route('/')
async def index(request):
    return await file('build/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, 
                    port=os.environ.get('PORT', 5000))
# ==========================================================