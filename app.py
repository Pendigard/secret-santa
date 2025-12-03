from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2.extras import DictCursor
import os
import random

app = Flask(__name__)
app.secret_key = 'impact_blabla_secret_key'
DATABASE = os.getenv('DATABASE_URL')

def init_db():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                target_id INTEGER,
                FOREIGN KEY (target_id) REFERENCES players(id)
            )
            ''')
            conn.commit()

def generate_random_string(length=5):
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    id = random.choice('abcdefghijklmnopqrstuvwxyz')
    for _ in range(length):
        char = random.choice(chars)
        if random.choice([True, False]):
            char = char.upper()
        id += char
    return id

def generate_unique_link_id():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            while True:
                link_id = generate_random_string()
                cursor.execute("SELECT 1 FROM players WHERE link_id = %s", (link_id,))
                if not cursor.fetchone():
                    return link_id

@app.route('/add', methods=['POST'])
def add():
    username = request.form['username']
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            link_id = generate_unique_link_id()
            cursor.execute("INSERT INTO players (username, link_id) VALUES (%s, %s)", (username, link_id))
            conn.commit()
    flash("Joueur ajouté.")
    return redirect('/8888')

@app.route('/8888')
def admin():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM players ORDER BY username ASC")
            players = cursor.fetchall()
    return render_template('index.html', players=players, admin=True)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)