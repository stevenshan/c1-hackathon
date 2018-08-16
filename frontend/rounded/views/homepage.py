from . import controller

@controller.route("/", methods=["GET"])
def homepage():
    return "TEST"

