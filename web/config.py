import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = "Rounded"
    SECRET_KEY = os.environ.get("SECRET_KEY")

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    REDIS_URL = os.environ.get("REDIS_URL")

    # capital one nessie api for bank transactions
    NESSIE_KEY = os.environ.get("NESSIE_KEY")

    CUSTOMER = "Jamey's Account"
    USER = "johnpaul"

    TWITTER = {
        "consumer_key": os.environ.get("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.environ.get("TWITTER_CONSUMER_SECRET"),
        "access_token": os.environ.get("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": os.environ.get("TWITTER_TOKEN_SECRET"),
    }

    RECOMBEE = (
        # database name
        os.environ.get("RECOMBEE_DB_NAME"),
        # secret token
        os.environ.get("RECOMBEE_SECRET_KEY"),
    )

    CHARITY_NAVIGATOR = {
        "app": os.environ.get("CHARITY_NAVIGATOR_APP"),
        "key": os.environ.get("CHARITY_NAVIGATOR_KEY"),
    }

    '''
    Database
    '''
    
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

