import plotly.graph_objs as go 
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
    

