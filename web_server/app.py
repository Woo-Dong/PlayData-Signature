
from sanic import Sanic 
from sanic_cors import CORS 
import sanic.response as Response

import json 
import os 

from functions.get_mongodb_data import *
from functions.plot_plotly import validate_fbprophet_plotly, predict_fbprophet_plotly


app = Sanic(__name__) 
app.static('', 'build') # After debugging, integrete with Sanic Framework 

# CORS enabled so react frontend can pull data from python backend
CORS(app)

@app.route('/api/test')
def hello_world(request):
    return Response.json({'res': 'Hello, World!'})

@app.route('/api/validate-fbprophet-plotly')
async def plot_validate_fbprophet_plotly(request):

    df = get_validate_fbprophet_data() 

    res = validate_fbprophet_plotly(df) 
    return Response.json(res)

@app.route('/api/predict-fbprophet-plotly')
async def plot_predict_fbprophet_plotly(request): 

    df, prev = get_predict_fbprophet_data() 

    res = predict_fbprophet_plotly(df, prev)

    return Response.json(res) 

@app.route('/api/dashboard')
async def dashboard(request): 
    res = get_dashboard_data()
    return Response.json(res)


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