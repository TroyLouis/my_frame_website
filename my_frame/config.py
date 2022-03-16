import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Config:
    SECRET_KEY = os.environ.get('MY_FRAME_SECRET_KEY') #set to environment export key etc
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #set to environment
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')