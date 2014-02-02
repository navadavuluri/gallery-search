from flask import Flask
import pg

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db_name= app.config['DB_NAME']

db = pg.connect(db_name, \
     app.config['DB_HOST'], \
     int(app.config['DB_PORT']), \
     None, None, \
     app.config['USERNAME'], \
     app.config['PASSWORD'] )


from app import views, models





