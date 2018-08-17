from rounded.mod_voting import controller

@controller.route("/", methods=["GET"])
def voting_list():
    return "HI"
