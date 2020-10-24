#!/usr/bin/env python3

import os
import subprocess
import flask
import time
import sys
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import core.config.manager as cfg_mgr


# Set config object
config = cfg_mgr.ConfigManager()

# Set stats dir
stats_dir = os.path.expanduser(config.stats_dir)
# TODO: remove this hardcode file nam
stats_file = os.path.abspath(os.path.join(
    stats_dir, 'includebeeredgeth.csv'))

data_refresh_rate = config.web.refresh_rate


app = flask.Flask(__name__)

@app.route('/')
def index():
      return flask.render_template('index.html', defaults=config.operating_dict)
    

app_dash = dash.Dash(__name__, server=app)



app_dash.layout = html.Div(children=[

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
   
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

])

@app_dash.callback(Output('live-text', 'children'),
                [Input('interval-component', 'n_intervals')])
def update_live_text(n):

    live_text = 'Current stats as of ' + \
        str(datetime.datetime.now())

    return live_text

@app_dash.callback(Output('graph-vessel-temperatures', 'figure'),
                   [Input('interval-component', 'n_intervals'), Input('url', 'pathname')])
def update_graph(n, pathname):
   
    df = pd.read_csv(stats_file)

    fig = px.line(df, x="timestamp", y="temperature")

    return fig

if __name__ == '__main__':

    app.run(host='0.0.0.0')
