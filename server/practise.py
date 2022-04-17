import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import jwt_required
from mysql.connector import Error

from server.db import get_db

bp = Blueprint("site", __name__)

@bp.route("/vocab")
@jwt_required()
def about():
    return jsonify({"question": "toki word", "options": ["wrong", "another wrong", "right"], "correct": "right"})