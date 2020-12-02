
from sanic import Sanic 
from sanic_cors import CORS 
import sanic.response as Response

import os 

from functions.get_mongodb_data import get_validate_fbprophet_data, get_predict_fbprophet_data
from functions.plot_plotly import validate_fbprophet_plotly, predict_fbprophet_plotly

from functions.get_mongodb_data import get_global_daily_data, get_global_cumul_data
from functions.plot_plotly import global_daily_plotly, global_cumul_plotly 


from functions.get_mongodb_data import get_domestic_daily_data, get_domestic_cumul_data
from functions.plot_plotly import domestic_cumul_age_plotly, domestic_cumul_area_plotly, domestic_cumul_gender_plotly
from functions.plot_plotly import domestic_daily_plotly


from functions.get_mongodb_data import get_news_summary, get_brefing_info 


from functions.get_mongodb_data import get_dashboard_data

app = Sanic(__name__) 
# app.static('', 'build') # After debugging, integrete with Sanic Framework 

# CORS enabled so react frontend can pull data from python backend
CORS(app)

@app.route('/api/test')
def hello_world(request):
    return Response.json({'res': 'Hello, World!'})

@app.route('/api/validate-fbprophet-plotly')
async def plot_validate_fbprophet_plotly(request):

    df, min_value, average, max_value = get_validate_fbprophet_data() 
    res = validate_fbprophet_plotly(df) 
    res['min_value'] = min_value 
    res['max_value'] = max_value 
    res['average'] = average
    
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


@app.route('/api/global-daily-plotly')
async def plot_global_daily_plotly(request): 
    
    df = get_global_daily_data()
    res = global_daily_plotly(df) 
    return Response.json(res)


@app.route('/api/global-cumul-plotly')
async def plot_global_cumul_plotly(request): 

    df, last_date = get_global_cumul_data()
    res = global_cumul_plotly(df, last_date) 
    
    return Response.json(res)

@app.route('/api/domestic-daily-plotly')
async def plot_domestic_daily_area_plotly(request): 

    req = request.args
    key, values = req['query'][0], req['y'][0]
    area_df, maximum, minimum = get_domestic_daily_data(key)

    res = domestic_daily_plotly(area_df, key, values)
    res['maximum'] = maximum
    res['minimum'] = minimum
    return Response.json(res) 

@app.route('/api/domestic-cumul-plotly')
async def plot_domestic_cumul_plotly(request): 

    req = request.args 
    key = req['query'][0] 

    ret_df = get_domestic_cumul_data(key)

    if key == 'area': res = domestic_cumul_area_plotly(ret_df) 
    elif key == 'age': res = domestic_cumul_age_plotly(ret_df) 
    else: res = domestic_cumul_gender_plotly(ret_df) 

    return Response.json(res)


@app.route('/api/news-summary')
async def news_summary(request): 
    res = dict(
        contents=get_news_summary() 
    )
    return Response.json(res)

@app.route('/api/brefing-info')
async def brefing_info(request): 
    res = get_brefing_info()
    return Response.json(res)


# Sanic Main Setting -> running app ========================
# @app.route('/')
# async def index(request):
#     return await Response.file('build/index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, 
                    port=os.environ.get('PORT', 5000))
# ==========================================================