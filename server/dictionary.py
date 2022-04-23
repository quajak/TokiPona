import functools
import json
import math

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import Error

from server.db import get_db

bp = Blueprint("dictionary", __name__, url_prefix="/api/dictionary")

@bp.route("/search")
def search():
    data = request.args
    word = data["word"]
    
    with get_db().cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("""
                       SELECT DISTINCT word
                       FROM word
                       WHERE toki = 1 AND word LIKE CONCAT(%s, '%')
                       """, (word, ))
        results = [w["word"] for w in cursor.fetchall()]
    return {"success": True, "results": results}
        
        
@bp.route("/define")
def define():
    data = request.args
    word = data["word"]
    
    with get_db().cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("""
                       SELECT *
                       FROM word
                       WHERE word = %s AND toki = 1
                       """, (word, ))
        word_obj = cursor.fetchall()
        
        if len(word_obj) == 0:
            return {"success": False, "error": "Word not found!"}
        
        definitions = []
        
        for word in word_obj:
            definition = {"type": word["type"]}
            cursor.execute("""
                           SELECT w.word
                           FROM word w
                            INNER JOIN vocab v
                            ON w.id = v.english
                            WHERE v.toki = %s;
                           """, (word["id"], ))
            english = [e["word"] for e in cursor.fetchall()]
            definition["english"] = english
            definitions.append(definition)
    
    return { "success": True, "definitions": definitions}