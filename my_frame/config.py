import os

class Config:
    SECRET_KEY = os.environ.get('MY_FRAME_SECRET_KEY') #set to environment export key etc
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #set to environment
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    S3_BUCKET = 'myframebucket'
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
