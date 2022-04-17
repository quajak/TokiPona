from mysql.connector import connect, MySQLConnection

import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext

def get_db() -> MySQLConnection:
    if "db" not in g:
        g.db = connect(
            host=current_app.config["DATABASE_HOST"],
            port=current_app.config["DATABASE_PORT"],
            user="root",
            password=current_app.config["DATABASE_PASSWORD"],
            database="toki_pona"
        )
    
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    
    if db is not None:
        db.close()
        
        
def init_db():
    db = get_db()
    with db.cursor() as cursor:
        with current_app.open_resource("schema.sql") as f:
            cursor.execute(f.read().decode("utf8"))
    
    
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing database and create a new one"""
    init_db()
    click.echo("Initialized database")
    
@click.command("init-dictionary")
@with_appcontext
def init_dictionary():
    db = get_db()
    with db.cursor() as cursor:
        with current_app.open_resource("./raw_data/dictionary.csv", "r") as file:
            for line in file.readlines():
                parts = line.strip().split("|")
                assert len(parts) == 3 or len(parts) == 4
                toki = parts[0].strip()
                type = parts[1].strip()
                cursor.execute("""
                                   INSERT INTO word
                                   (word, toki, type, official)
                                   VALUES (%s, %s, %s, %s);
                                   """, (toki, True, type, len(parts) == 3))
                db.commit()
                for english in parts[2].split(","):
                    english = english.strip()
                    cursor.execute("""
                                   INSERT INTO word (word, toki)
                                   SELECT * FROM (SELECT %s, false) AS tmp
                                   WHERE NOT EXISTS ( SELECT * FROM word WHERE word = %s AND toki = 0);
                                   """, (english, english))
                    db.commit()
                    cursor.execute("""
                                   INSERT INTO vocab (english, toki)
                                   WITH toki AS (
                                       SELECT id FROM word
                                       WHERE word = %s AND type = %s
                                   ),
                                   english AS (
                                       SELECT id FROM word
                                       WHERE word = %s
                                   )
                                   SELECT english.id, toki.id FROM toki, english;
                                   """, (toki, type, english))
                    db.commit()
    print("Loaded dictionary")
            
    
def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_dictionary)
