import os
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    current_dir = os. getcwd()
    return render_template('index.html', current_dir=current_dir)


@bp.route("/<session_id>")
def session(session_id):
    return render_template('session.html', session_id=session_id)
