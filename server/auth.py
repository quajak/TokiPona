import functools
from datetime import datetime, timedelta, timezone

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, jsonify
)
from flask_jwt_extended import (
    create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, JWTManager,
    unset_access_cookies, get_jwt_identity, jwt_required, get_jwt
)
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector import Error

from server.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

def assign_access_refresh_tokens(user_id: int):
    access_token = create_access_token(identity=str(user_id))
    resp = make_response(jsonify({"success": True}))
    set_access_cookies(resp, access_token)
    return resp
    
def unset_jwt():
    resp = make_response(jsonify({"success": True, "no_jwt": True}))
    unset_access_cookies(resp)
    return resp

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    
    db = get_db()
    error = None
    
    if not username:
        error = "Username is required"
    elif len(username) > 30:
        error = "Username must be less than 31 characters"
    elif not password:
        error = "Password must be set"
    elif len(password) > 127:
        error = "Password must be shorter than 128 characters"
        
    if error is None:
        with db.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)", (username, generate_password_hash(password))
                )
                db.commit()
            except Error:
                error = "Username already exists"
            
            # now initialize learning progress
            
            cursor.execute("SELECT id FROM user WHERE username = %s", (username, ))
            user_id = cursor.fetchone()

            cursor.execute(
                """
                INSERT INTO vocab_progress (vocab, user)
                (SELECT id, %s from vocab)
                """, user_id
            )
            db.commit()

            if error is None:
                return jsonify({"success": True})
    return jsonify({"success": False, "error": error})


@bp.route("/login", methods=["POST"])
def login():
    print("Login attempt")
    if g.user is not None:
        return jsonify({"success": False, "error": "Already logged in"})    
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    
    db = get_db()
    error = None
    
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("SELECT * FROM user WHERE username = %s", (username, ))
        user = cursor.fetchone()
        
    if user is None:
        error = "Incorrect username"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
        
    if error is None:
        session.clear()
        session["user_id"] = user["id"]
        return assign_access_refresh_tokens(user["id"])
    
    return jsonify({"success": False, "error": error})
    
@bp.route("/user", methods=["GET"])
@jwt_required()
def user():
    return jsonify({"username": g.user["username"]})
    
@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return unset_jwt()

@bp.route("/refresh")
@jwt_required()
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    resp = make_response(redirect("/"))
    set_access_cookies(resp, access_token)
    return resp
    
@bp.before_app_request
@jwt_required(optional=True)
def load_logged_in_user():
    if request.method == "OPTIONS":
        g.user = None
        return
    user_id = get_jwt_identity()
    
    if user_id is None:
        g.user = None
    else:
        with get_db().cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT * FROM user where id = %s", (user_id,))
            g.user = cursor.fetchone()
            
            
@bp.after_request
def refresh_expiring_jwts(response):
    try:
        data = response.get_json()
        if data is not None and "no_jwt" in data and data["no_jwt"]:
            return response
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response