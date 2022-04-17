import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from mysql.connector import Error
from server.auth import login_required

from server.db import get_db

bp = Blueprint("site", __name__)

@bp.route("/")
def index():
    return render_template("site/index.html")

@bp.route("/about")
def about():
    return render_template("site/about.html")