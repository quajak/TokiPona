import functools
import json
import math

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import Error
from random import randint

from server.db import get_db

bp = Blueprint("practise", __name__, url_prefix="/api")

@bp.route("/get_vocab_pair")
@jwt_required()
def vocab_pair():
    user_id = get_jwt_identity()
    data = request.args
    mode = data["mode"]
    
    with get_db().cursor(dictionary=True, buffered=True) as cursor:
        vocab = get_word_to_test(user_id, mode, cursor)
        
        cursor.execute(
            """
            SELECT word
            FROM word
            WHERE id = %s
            """, (vocab["toki"],)
        )
        toki = cursor.fetchone()["word"]
        
        cursor.execute(
            """
            SELECT word
            FROM word
            WHERE id = %s
            """, (vocab["english"],)
        )
        english = cursor.fetchone()["word"]
    return {"toki": toki, "english": english, "id": vocab["id"]}

@bp.route("/vocab")
@jwt_required()
def vocab():
    user_id = get_jwt_identity()
    data = request.args
    mode = data["mode"]
    options = int(data["options"])
    
    with get_db().cursor(dictionary=True, buffered=True) as cursor:
        vocab = get_word_to_test(user_id, mode, cursor)
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
            LIMIT %s;
            """, (toki["word"], options - 1)
        )
        wrong_english = [option["word"] for option in cursor.fetchall()]
    
    return {"toki": toki["word"], "correct_english": english["word"], "other_options": wrong_english, "vocab_id": vocab["id"]}

def get_word_to_test(user_id, mode, cursor):
    if mode == "All":
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
    elif mode == "Mistakes":
        cursor.execute(
                """
                    SELECT vocab 
                    FROM vocab_progress
                    WHERE user = %s
                    ORDER BY
                    streak ASC,
                    correct ASC,
                    RAND() ASC
                    LIMIT 1;
                """, (user_id, ))
    else:
        raise Exception("Not a valid mode: " + mode)
    vocab_id = cursor.fetchone()["vocab"]
    
    cursor.execute(
    """
    SELECT * 
    FROM vocab
    WHERE id = %s;
    """, (vocab_id,)
    )
    vocab = cursor.fetchone()
    return vocab

@bp.route("/practise", methods=["POST"])
@jwt_required()
def practise():
    user_id = get_jwt_identity()
    
    data = request.get_json()
    vocab_id = data["vocab_id"]
    correct = data["correct"]
    type = data["type"]
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
                        tries = tries + 1,
                        streak = %s
                        WHERE id = %s
                       """, (vocab_progress["correct"] + 1 if correct else 0, vocab_progress["streak"] + 1 if correct else min(-1, vocab_progress["streak"] - 1), vocab_progress["id"]), )
        if type != -1:
            if correct:
                cursor.execute("""
                            SELECT *
                            FROM streaks
                            WHERE user = %s AND active = 1 AND type = %s
                            """, (user_id, type))
                streaks = cursor.fetchone()
                if streaks is None:
                    cursor.execute("""
                                INSERT INTO streaks
                                (user, correct, type)
                                VALUES (%s, 1, %s)
                                """, (user_id, type))
                else:
                    cursor.execute("""
                                UPDATE streaks
                                SET correct = correct + 1
                                WHERE user=%s AND active = 1 AND type = %s
                                """, ((user_id, type)))
            else:
                cursor.execute("""
                            UPDATE streaks
                            SET active = 0
                            WHERE user = %s AND type = %s
                            """, ((user_id, type)))
        db.commit()
        
    return jsonify({"success": True, "streak": get_streak(user_id, type)})

def get_streak(user_id: int, type: int):
    db = get_db()
    with db.cursor(dictionary=True, buffered=True) as cursor:    
        cursor.execute("""
                    SELECT correct
                    FROM streaks
                    WHERE user = %s AND active = 1 AND type = %s
                    """, ((user_id, type)))
        count = cursor.fetchone()
    return count["correct"] if count is not None else 0

@bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    db = get_db()
    scores = {}
    
    with db.cursor(dictionary=True, buffered=True) as cursor:
        scores["0"] = get_streak_info(user_id, cursor, 0)
        scores["1"] = get_streak_info(user_id, cursor, 1)
        cursor.execute("""
                       SELECT SUM(correct)
                       FROM vocab_progress
                       WHERE user = %s
                       """, (user_id, ))
        progress = int(cursor.fetchone()["SUM(correct)"])
    return jsonify({"scores": scores, "progress": progress})

def get_streak_info(user_id, cursor, type):
    streak = get_streak(user_id, type)
    cursor.execute("""
                       SELECT correct
                       FROM streaks
                       WHERE user = %s AND type = %s
                       ORDER BY correct DESC
                       LIMIT 1;
                       """, (user_id, type))
    if best := cursor.fetchone():
        best = best["correct"]
    else:
        best = 0
    info = {"best": best, "current": streak}
    return info


@bp.route("/selectall", methods=["GET"])
@jwt_required()
def selectall():
    user_id = get_jwt_identity()
    
    db = get_db()
    
    num_correct= randint(3,7)
    num_wrong  = 15 - num_correct
    
    with db.cursor(dictionary=True, buffered=True) as cursor:
        cursor.execute(
            """
                SELECT word 
                FROM word
                WHERE toki = 1
                ORDER BY
                RAND() ASC
                LIMIT 1;
            """)

        vocab_word = cursor.fetchone()["word"]
        cursor.execute(
            """
            SELECT *
                FROM (
                    SELECT e.word, v.id
                    FROM word e
                        INNER JOIN vocab v
                        ON e.id = v.english
                            INNER JOIN word w
                            ON w.id = v.toki
                            WHERE w.word = %s AND w.toki = 1
                    ORDER BY RAND() ASC
                ) diff_words
            GROUP BY diff_words.word
            ORDER BY RAND() ASC
            LIMIT %s;
            """, (vocab_word, num_correct)
        )
        correct_english = cursor.fetchall()
        num_wrong  = 15 - len(correct_english)
        
        cursor.execute(
            """
            SELECT *
                FROM (
                    SELECT e.word, v.id
                    FROM word e
                        INNER JOIN vocab v
                        ON e.id = v.english
                            INNER JOIN word w
                            ON w.id = v.toki
                            WHERE w.word != %s AND w.toki = 1
                    ORDER BY RAND() ASC
                ) diff_words
            GROUP BY diff_words.word
            ORDER BY RAND() ASC
            LIMIT %s;
            """, (vocab_word, num_wrong)
        )
        wrong_english = cursor.fetchall()
        
    return jsonify({"success": True, "correct_english": correct_english, "other_options": wrong_english, "toki": vocab_word})