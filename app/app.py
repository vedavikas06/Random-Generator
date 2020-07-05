from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from get_number import router as fapi
from flask_login import LoginManager
# from flask_limiter import Limiter
import uvicorn, os
from datetime import timedelta

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# Initialize flask_app
app = Flask(__name__)
# limiter = Limiter(app)

#Set Config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '86447cee46f2817299f39ae5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds = 10)


db.init_app(app)


#Atatch Login manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from models import User
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return abort(403, description="Please Login to use the API")


# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for main parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)


#fastapi routes (/get_random)
fast_app = FastAPI()
fast_app.include_router(fapi)
fast_app.mount("", WSGIMiddleware(app))


if __name__ == "__main__":
    
    logger.debug("Starting the Application")
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("app:fast_app", host="0.0.0.0", port=port,reload=True)


