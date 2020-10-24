import os
import time
import sys
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# stats_dir = './data'

def register_callbacks(app_dash, config, brew):

    # Set stats dir
    stats_dir = os.path.expanduser(config.defaults.stats_dir)

    @app_dash.callback(Output('session-text', 'children'),
                    [Input('url', 'pathname')])
    def update_session_text(pathname):
        _session = pathname.split('/')[2]
        # brew_session = next(filter(
        #     lambda session: session.get('id') == _session, brew.sessions), None)

        # text = 'Brew session: ' + brew_session['name']
        text = 'Brew session: ' + _session

        return html.H1(children=text)

    @app_dash.callback(Output('live-text', 'children'),
                    [Input('interval-component', 'n_intervals')])
    def update_live_text(n):

        live_text = 'Current stats as of ' + \
            str(datetime.datetime.now())

        return live_text

    @app_dash.callback(Output('links-text', 'children'),
                       [Input('url', 'pathname')])
    def update_links_text(pathname):
        _session = pathname.split('/')[2]
        return [
                html.A(href='/', children='Home'),
                html.Br(),
                html.A(href='/' + _session, children='Session Home')]

    @app_dash.callback(Output('graph-vessel-temperatures', 'figure'),
                    [Input('interval-component', 'n_intervals'), Input('url', 'pathname')])
    def update_graph(n, pathname):
        _session = pathname.split('/')[2]
        # brew_session = next(filter(
        #     lambda session: session.get('id') == _session, brew.sessions), None)

        # stats_file = os.path.abspath(os.path.join(
        #     stats_dir, brew_session['id'] + '_' + brew_session['stage'] + '.csv'))
        # stats_file = os.path.abspath(os.path.join(
        #     stats_dir, _session + '_primary.csv'))
        # df = pd.read_csv(stats_file)

        # fig = px.line(df, x="timestamp", y="vessel_temperature", color="vessel")
        stats_file = os.path.abspath(os.path.join(
            stats_dir, 'includebeeredgeth.csv'))

        df = pd.read_csv(stats_file)

        fig = px.line(df, x="timestamp", y="temperature")

        return fig


