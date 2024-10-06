from flask import Flask
from models import db
from config import Config
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)


if __name__ == '__main__':
    app.run(debug=True, port=6000)

