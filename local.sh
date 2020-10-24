# local.sh

export FLASK_APP=wsgi
export FLASK_DEBUG=1
export INCLUDE_BEER_CONFIG=./include-beer.yml
flask run