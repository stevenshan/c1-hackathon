import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = "Rounded"
    SECRET_KEY = "########"

    REDIS_URL = "redis://h:p633e4fabfec649572dc5def69168418c21558611dc98ed1f1bf848198c5ba8b0@ec2-52-5-241-209.compute-1.amazonaws.com:15939"

    CUSTOMER = "Jamey's Account"

    '''
    Database
    '''
    
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

"""
Import configuration variables from system environment variables
"""

Config.SECRET_KEY = os.environ.get("SECRET_KEY", Config.SECRET_KEY)
