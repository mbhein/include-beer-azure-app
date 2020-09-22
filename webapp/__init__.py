"""Initialize Flask app."""
import os
import dash
from flask import Flask
from flask import render_template
from flask.helpers import get_root_path

import modules.config.manager as cfg_mgr
import modules.config.sessions as sessions_mgr
from modules.utils.dicts import DotNotation as DotNotation

# Set config object
config = cfg_mgr.ConfigManager()

# Set Brew sessions
brew = sessions_mgr.SessionsManager()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



def init_app(test_config=None):

    

    # Set stats dir
    stats_dir = os.path.expanduser(config.defaults.stats_dir)
    data_refresh_rate = config.web.data_refresh_rate

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # default secret that should be overriden by instance
        SECRET_KEY="dev"
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)


    # apply the blueprints to the app
    from webapp import brewery
    app.register_blueprint(brewery.bp)

    app.add_url_rule("/", endpoint="index")

    # load in dash stats
    register_app_dash(app)

    return app

def register_app_dash(app):
    from webapp.dashstats.layouts import layout
    from webapp.dashstats.callbacks import register_callbacks
    app_dash = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/stats/',
                        external_stylesheets=external_stylesheets)

    with app.app_context():
        app_dash.title = "Session Stats"
        app_dash.layout = layout
        register_callbacks(app_dash, config, brew)
        

app = init_app()

