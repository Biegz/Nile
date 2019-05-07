from flask import Flask
from flask_bootstrap import Bootstrap
import pymysql.cursors

app = Flask(__name__)
Bootstrap(app)

connection = pymysql.connect(host='niledbinstance.cuc9g3dewtdp.us-east-2.rds.amazonaws.com',
                             user='abiegler',
                             password='password',
                             db='default_schema',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

from app import routes
