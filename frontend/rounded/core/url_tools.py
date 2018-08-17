import flask
from rounded.core import user

def render_template(*argv, **kwargs):

    kwargs["current"] = user.getCharity()

    return flask.render_template(*argv, **kwargs)

