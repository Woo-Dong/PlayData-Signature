from plotly.subplots import make_subplots
import plotly.graph_objs as go 
import plotly.express as px

import json 

def validate_fbprophet_plotly(data_df): 

    trace_lower = go.Scatter( 
        x=data_df.date, 
        y=data_df.lower, 
        name='하한 예측값'
    )

    trace_upper = go.Scatter( 
        x=data_df.date, 
        y=data_df.upper, 
        name='상한 예측값'
    )

    trace_pred = go.Scatter(
        x=data_df.date, 
        y=data_df.pred,
        name='예측 값', mode='markers'
    )

    trace_real = go.Scatter(
        x=data_df.date, 
        y=data_df.real,
        name='실제 값', mode='markers'
    )

    plot_data = [trace_lower, trace_upper, trace_pred, trace_real]

    colors = ['#0a01ff', '#989cff', '#0a9cff', '#ff0000']

    layout = go.Layout(
        # title= "코로나 확진 누적 예측",
        yaxis=dict(
            title='확진자 수',
            titlefont=dict(color=colors[0]),
            tickfont=dict(color=colors[0])
        ),
        yaxis2=dict(
            title='pred',
            overlaying='y',
            side='right',
            titlefont=dict(color=colors[1]),
            tickfont=dict(color=colors[1])    
        ), 
        yaxis3=dict(
                title='real',
                overlaying='y',
                side='right',
                titlefont=dict(color=colors[2]),
                tickfont=dict(color=colors[2])    
            ),
        yaxis4=dict(
                title='upper',
                overlaying='y',
                side='right',
                titlefont=dict(color=colors[3]),
                tickfont=dict(color=colors[3])    
            )
    )

    fig = go.Figure(data=plot_data, layout=layout)
    fig.update_layout(barmode='group', hovermode='x')

    json_str = fig.to_json() 
    return json.loads(json_str) 


def predict_fbprophet_plotly(data_df, prev_num): 

    col_list = ['date', 'pred', 'lower', 'upper']

    for col in col_list[1:]: 
        data_df[col] = data_df[col] - prev_num
        data_df[col] = round(data_df[col].clip(0), 0)

    date = data_df.date.to_list() 
    date_rev = date[::-1]

    trace_err = go.Scatter( 
        x=date+date_rev, 
        y=data_df.upper.to_list()+data_df.lower.to_list()[::-1], 
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
    #     showlegend=False,
        name='예측 범위'
    )

    trace_pred = go.Scatter(
        x=data_df.date, 
        y=data_df.pred,
        name='예측 값', mode='markers'
    )

    plot_data = [trace_err, trace_pred]

    fig = go.Figure(data=plot_data)

    json_str = fig.to_json() 
    return json.loads(json_str)
    

def global_daily_plotly(data_df): 


    fig = px.line(data_df, x='date', y='confirmed', color='country',
              title='Global daily recently',
              hover_name='country')

    fig.update_layout(
        plot_bgcolor="white", 
        autosize=False, 
        width=600, 
        height=350
    )
    json_str = fig.to_json()
    return json.loads(json_str)


def global_cumul_plotly(data_df, last_date): 

    countries = list(data_df.country.unique())

    fig = go.Figure(data=[
        go.Bar(name='confirmed', x=countries, y=data_df.confirmed), 
        go.Bar(name='deaths', x=countries, y=data_df.deaths),
        go.Bar(name='recovered', x=countries, y=data_df.recovered*(-1),
            base=0),
    ])

    fig.update_layout(barmode='stack', title='Global Cumulative, date:'+last_date, 
        autosize=False, 
        width=600, 
        height=350
    )

    json_str = fig.to_json()
    return json.loads(json_str)


# domestic_daily_age_confirmed_plotly(data_df, 'age', 'confirmed')
def domestic_daily_plotly(data_df, key, val): 

    fig = px.line(data_df, x='date', y=val, color=key,
                  title='Domestic daily ' + key,
                  hover_name=key)
    fig.update_layout(
        plot_bgcolor="white", 
        legend={'traceorder': 'normal'}, 
        autosize=False, 
        width=600, 
        height=350
    )
    json_str = fig.to_json()  
    return json.loads(json_str)


def domestic_cumul_age_plotly(data_df): 

    ages = data_df.attr.unique() 

    fig = go.Figure(data=[
        go.Bar(x=ages, y=data_df.confirmed, name='confirmed'),
        go.Bar(x=ages, y=data_df.death, name='death')
    ])

    fig.update_layout(
        title='domestic cumul: age',
        barmode='group', 
        autosize=False, 
        width=600, 
        height=350
    )
    json_str = fig.to_json() 
    return json.loads(json_str) 

def domestic_cumul_area_plotly(data_df): 

    areas = data_df.attr.unique()

    fig = go.Figure(data=[
        go.Bar(name='confirmed', x=areas, y=data_df.confirmed), 
        go.Bar(name='death', x=areas, y=data_df.death),
        go.Bar(name='released', x=areas, y=data_df.released*(-1),
            base=0),
    ])

    fig.update_layout(barmode='stack', title='domestic cumul: area',
        autosize=False, 
        width=600, 
        height=350
    )
    
    json_str = fig.to_json() 
    return json.loads(json_str)

def domestic_cumul_gender_plotly(data_df): 

    data_df.sort_values('attr', axis=0, inplace=True)
    genders = data_df.attr.unique()
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=genders, values=data_df.confirmed, name="confirmed"), 
                1, 1)
    fig.add_trace(go.Pie(labels=genders, values=data_df.death, name="death"),
                1, 2)
    fig.update_layout(
        title_text="domestic cumul: gender",
        legend={'traceorder': 'reversed'},
        autosize=False, 
        width=600, 
        height=350
    )
    fig.update_traces(
        marker=dict(colors=['#636EFA', '#EF553B'])) 
    json_str = fig.to_json() 
    return json.loads(json_str)     