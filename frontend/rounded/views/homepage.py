from . import controller
from rounded.core import url_tools
import flask

@controller.route("/", methods=["GET"])
def homepage():
    return url_tools.render_template("base_page.html")

