# local.sh

export FLASK_APP=wsgi:app
export FLASK_DEBUG=1
export INCLUDE_BEER_SESSION_FILE=./data/include-beer-sessions.yml
export INCLUDE_BEER_STATS_DIR=./data
flask run