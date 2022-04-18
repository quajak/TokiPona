from datetime import timedelta
import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, unset_access_cookies


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    with open("./secrets/flask.txt") as file:
        secret_key = file.readline().strip()

    with open("./secrets/database_password.txt") as file:
        database_password = file.readline().strip()
        
    with open("./secrets/jwt_secret_key.txt") as file:
        jtw_secret_key = file.readline().strip()

    db_host = os.getenv("DB_HOST")
    if db_host is None:
        db_host = "127.0.0.1"

    app.config.from_mapping(
        SECRET_KEY = secret_key,
        DATABASE_PORT = "3306",
        DATABASE_HOST = db_host,
        DATABASE_PASSWORD = database_password,
        JWT_SECRET_KEY = jtw_secret_key,
        JWT_TOKEN_LOCATION = ["cookies"],
        JWT_COOKIE_CSRF_PROTECT = True,
        JWT_CSRF_CHECK_FORM = True,
        JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN",
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import practise
    app.register_blueprint(practise.bp)
    
    CORS(app, resources={r'/*': {'origins': 'localhost'}})
    
    jwt = JWTManager(app)
    
    @jwt.expired_token_loader
    def expired_token_callback(header, data):
        res = jsonify({"success": False, "error": "The token has expired"})
        unset_access_cookies(res)
        return res, 401
    
    @app.route("/hello")
    def hello():
        return jsonify({"hello": "world"})
    
    return app
