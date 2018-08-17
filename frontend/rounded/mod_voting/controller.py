import flask
from rounded.core import url_tools

mod_voting = flask.Blueprint("mod_voting", __name__)

def route(*argv, **kwargs):
    '''
    wrapper around flask.Blueprint.route
    '''

    return mod_voting.route(*argv, **kwargs)

#######################################
# Import each view
#######################################

from rounded.mod_voting.views import *

