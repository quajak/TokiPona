import functools
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import Error

from server.db import get_db

bp = Blueprint("practise", __name__)

@bp.route("/vocab")
@jwt_required()
def vocab():
    user_id = get_jwt_identity()
    
    with get_db().cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute(
            """
                SELECT vocab 
                FROM vocab_progress
                WHERE user = %s
                ORDER BY
                correct ASC,
                RAND() ASC
                LIMIT 1;
            """, (user_id, ))
        vocab_id = cursor.fetchone()["vocab"]
        cursor.execute(
            """
            SELECT * 
            FROM vocab
            WHERE id = %s;
            """, (vocab_id,)
        )
        vocab = cursor.fetchone()
        cursor.execute(
            """
            SELECT word
            FROM word
            WHERE id = %s
            """, (vocab["toki"],)
        )
        toki = cursor.fetchone()
        cursor.execute(
            """
            SELECT word 
            FROM word
            WHERE id = %s
            """, (vocab["english"],)
        )
        english = cursor.fetchone()
        cursor.execute(
            """
            SELECT w.word
                        FROM word w
                            INNER JOIN vocab v
                                on w.id = v.english
                                INNER JOIN word j
                                    on v.toki = j.id
                                    WHERE j.word != %s
            ORDER BY RAND()
            LIMIT 3;
            """, (toki["word"],)
        )
        wrong_english = [option["word"] for option in cursor.fetchall()]
    
    return {"toki": toki["word"], "correct_english": english["word"], "other_options": wrong_english, "vocab_id": vocab_id}

@bp.route("/practise", methods=["POST"])
@jwt_required()
def practise():
    user_id = get_jwt_identity()
    
    data = request.get_json()
    vocab_id = data["vocab_id"]
    correct = data["correct"]
    db = get_db()
    
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute("""
                       SELECT *
                       FROM vocab_progress
                       WHERE vocab = %s AND user = %s
                       """, (vocab_id, user_id, ))
        vocab_progress = cursor.fetchone()
        cursor.execute("""
                       UPDATE vocab_progress
                       SET
                        correct = %s,
                        tries = %s
                        WHERE id = %s
                       """, (vocab_progress["correct"] + 1 if correct else 0, vocab_progress["tries"] + 1, vocab_progress["id"]), )
        db.commit()
        
    return jsonify({"success": True})