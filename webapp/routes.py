"""Routes for Flask side of the webapp"""
import os
from flask import render_template
from flask import current_app as app

current_dir = os. getcwd()

@app.route('/')
def index():
    return render_template('index.html', current_dir=current_dir)
