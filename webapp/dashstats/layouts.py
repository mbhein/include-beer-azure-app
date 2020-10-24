import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

data_refresh_rate = 300

layout = html.Div(children=[

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    #html.Div(id='session-text'),

    html.Div(id='live-text'),
    
    dcc.Graph(
        id='graph-vessel-temperatures'
    ),
    dcc.Interval(
        id='interval-component',
        interval=data_refresh_rate*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(children='Data refresh rate (in seconds): ' +
            str(data_refresh_rate),),

    html.Div(id='links-text'),
    
    ])
