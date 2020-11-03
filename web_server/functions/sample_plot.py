from bokeh.plotting import Figure
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.sampledata.autompg import autompg
from numpy import cos, linspace
import json

def get_plot_sample1(): 

    # copy/pasted from Bokeh Getting Started Guide - used as an example
    grouped = autompg.groupby("yr")
    mpg = grouped.mpg
    avg, std = mpg.mean(), mpg.std()
    years = list(grouped.groups)
    american = autompg[autompg["origin"]==1]
    japanese = autompg[autompg["origin"]==3]

    p = Figure(title="MPG by Year (Japan and US)", plot_width=400, plot_height=800)

    p.vbar(x=years, bottom=avg-std, top=avg+std, width=0.8, 
        fill_alpha=0.2, line_color=None, legend="MPG 1 stddev")

    p.circle(x=japanese["yr"], y=japanese["mpg"], size=10, alpha=0.5,
            color="red", legend="Japanese")

    p.triangle(x=american["yr"], y=american["mpg"], size=10, alpha=0.3,
            color="blue", legend="American")

    p.legend.location = "top_left"
    return json_item(p, "myplot")


def get_plot_sample2(): 
    # copy/pasted from Bokeh 'JavaScript Callbacks' - used as an example
    # https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html
    x = [x*0.005 for x in range(0, 200)]
    y = x

    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = Figure(plot_width=400, plot_height=800)
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var f = cb_obj.value
        var x = data['x']
        var y = data['y']
        for (var i = 0; i < x.length; i++) {
            y[i] = Math.pow(x[i], f)
        }
        source.change.emit();
    """)

    slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
    slider.js_on_change('value', callback)
    layout = column(slider, plot)

    return json_item(layout, "myplot")