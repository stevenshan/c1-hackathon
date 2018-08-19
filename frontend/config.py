import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = "Rounded"
    SECRET_KEY = os.environ.get("SECRET_KEY")

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

    REDIS_URL = os.environ.get("REDIS_URL")

    CUSTOMER = "Jamey's Account"
    USER = "johnpaul"

    '''
    Database
    '''
    
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

