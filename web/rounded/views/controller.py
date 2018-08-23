import flask

# create blueprint to register routes to
views = flask.Blueprint("app", __name__)

# wrapper around flask.Blueprint.route
def route(*argv, **kwargs):
    return views.route(*argv, **kwargs)

