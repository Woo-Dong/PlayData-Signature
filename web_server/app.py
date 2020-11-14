
from sanic import Sanic 
import sanic.response as Response
from sanic_cors import CORS 

from sanic_scheduler import SanicScheduler, task 

from datetime import datetime, time, timedelta 

import os 

from functions.get_data import *
from functions.plot_to_bokeh import *
from functions.cron_job_crawling import *
from functions.cron_job_inference import * 


app = Sanic(__name__) 
app.static('', 'build') # After debugging, integrete with Sanic Framework 


# CORS enabled so react frontend can pull data from python backend
CORS(app)


scheduler = SanicScheduler(app)  # Cron Job Scheduler Setting 


@task(timedelta(seconds=30))
async def cron_inference(_): 
    # insert_inference_data(predict_fbprophet('sample'))
    print("Foo ", datetime.now()) 


@app.route('/api/test')
def hello_world(request):
    return Response.json({'res': 'Hello, World!'})


@app.route('/api/pred-fbprophet')
async def plot_predict_fbprophet(request):

    real_df = get_confirmed_data() 
    pred_df = get_predict_fbprophet_data() 

    res = get_plot_predict_fbprophet(real_df, pred_df)
    return Response.json(res)

@app.route('/api/dashboard')
async def dashboard(request): 
    res = get_dashboard_data()
    return Response.json(res)

# @app.route('/api/plot1')
# async def plot1(request):
#     return json(get_plot_sample1())


# @app.route('/api/news-data')
# async def news_data(request): 
#     return json(get_news_data())

# Sanic Main Setting -> running app ========================
@app.route('/')
async def index(request):
    return await Response.file('build/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, 
                    port=os.environ.get('PORT', 5000))
# ==========================================================