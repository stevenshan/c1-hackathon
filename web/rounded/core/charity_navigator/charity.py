class Charity:
  def __init__(self, mydict):
    self.dict = mydict
    self.name = mydict['charityName']
    self.id = mydict['ein']
    self.cause = mydict['cause']['causeID']
    self.mission = mydict['mission']
    self.state = mydict['mailingAddress']['stateOrProvince']