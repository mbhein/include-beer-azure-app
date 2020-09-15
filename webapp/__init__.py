"""Initialize Flask app."""
from flask import Flask
# from flask_assets import Environment


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
    

    with app.app_context():
        # Import routes of webapp
        from . import routes

        # Import stats
        # from .webapp import stats
        # app = init_dashboard(app)

        return app
