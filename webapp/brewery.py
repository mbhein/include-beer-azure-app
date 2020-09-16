import os
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
import modules.config.manager as cfg_mgr
import modules.config.sessions as sessions_mgr
from modules.utils.dicts import DotNotation as DotNotation

# Set config object
config = cfg_mgr.ConfigManager()

# Set Brew sessions
brew = sessions_mgr.SessionsManager()

bp = Blueprint("brewery", __name__)


@bp.route("/")
def index():
    current_dir = os. getcwd()
    return render_template('index.html', sessions=brew.sessions)


@bp.route("/<session_id>")
def session(session_id):
    brew_session = next(filter(
        lambda session: session.get('id') == session_id, brew.sessions), None)

    return render_template('session.html', session_id=session_id, session=brew_session)
