from flask import Flask, g, request
from flask_restful import Resource, Api
import sqlite3, os
# import logging
# from logging.handlers import RotatingFileHandler

app = Flask('imageapi') # create the application instance :)app = Flask(__name__) # create the application instance :)
app.config.from_object('imageapi') # load config from this file , flaskr.py
api = Api(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sunspot.db')
))

app.config.from_envvar('IMAGEAPI_SETTINGS', silent=True)

# Configure logging
# initialize the log handler
# logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
#
# # set the log handler level
# logHandler.setLevel(logging.INFO)
#
# # set the app logger level
# app.logger.setLevel(logging.INFO)
#
# app.logger.addHandler(logHandler)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


class Landmarks(Resource):
    def get(self):
        conn = get_db().cursor() # connect to database
        n = request.args.get('n')
        query = conn.execute( "select * from (select * from landmark_queue order by random()) order by n_distribute asc limit {}".format(n))
        #app.logger.info(query)
        result = query.fetchall()
        ids = ['"{}"'.format(i['landmarkId']) for i in result]
        increment_command = 'update landmark_queue set n_distribute = n_distribute + 1 where landmarkId in ({})'.format(', '.join(ids))
        # app.logger.info(increment_command)
        conn.execute(increment_command)
        get_db().commit()

        return {'description': [i['html_formatting'] for i in result],
                'OrgUrl': [i['imgURL'] for i in result],
                'landmarkId': [i['landmarkId'] for i in result]}

api.add_resource(Landmarks, '/landmarks')



