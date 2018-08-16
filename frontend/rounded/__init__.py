from flask import Flask

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

    # load configuration
    configMode = os.environ.get("app_configuration", "Config")
    app.config.from_object("config." + str(configMode))

    with app.app_context():
        # database setup
        from rounded.models import db
        db.init_app(app)
        migrate = flask_migrate.Migrate(app, db)

        # default app related views
        from rounded.views.controller import views

        # register controller blueprinters
        app.register_blueprint(views)

    return app
