from flask import Flask
from rounded.core import redis
from flask_googlemaps import GoogleMaps

# Database
import flask_migrate

# for getting environment variables
import os

###########################################################
# Setup App
###########################################################

def create_app():
    app = Flask(
        __name__,
        static_url_path="/static",
        instance_relative_config=True
    )

    GoogleMaps(app, key="AIzaSyADCxm6oxGCYP94Gq7igqtczUDycRvTbJU")
    
    # load configuration
    configMode = os.environ.get("app_configuration", "Config")
    app.config.from_object("config." + str(configMode))

    with app.app_context():
        # database setup
        from rounded.models import db
        db.init_app(app)
        migrate = flask_migrate.Migrate(app, db)

        # firebase.connect()
        redis.init()

        # default app related views
        from rounded.views.controller import views

        # import other blueprints
        from rounded.mod_voting.controller import mod_voting

        # register controller blueprinters
        app.register_blueprint(views)
        app.register_blueprint(mod_voting, url_prefix="/voting")

    return app
