from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2.extras import DictCursor
import os
import random

app = Flask(__name__)
app.secret_key = 'impact_blabla_secret_key'
DATABASE = os.getenv('DATABASE_URL')

def drop_db():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS players')
            conn.commit()


def init_db():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                target_id INTEGER,
                link_id TEXT UNIQUE NOT NULL,
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
            cursor.execute("SELECT username FROM players WHERE username = %s", (username,))
            if cursor.fetchone():
                flash("Ce nom d'utilisateur existe déjà.")
                return redirect('/8888')
            cursor.execute("INSERT INTO players (username, link_id) VALUES (%s, %s)", (username, link_id))
            conn.commit()
    flash("Joueur ajouté.")
    return redirect('/8888')

@app.route('/delete/<int:player_id>')
def delete_player(player_id):
    print(player_id)
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE players SET target_id = NULL WHERE target_id = %s", (player_id,))
            cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
            conn.commit()
    flash("Joueur supprimé avec succès.")
    return redirect('/8888')

def assign_ids(players, id_param):
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            players_list = [player['id'] for player in players]
            random.shuffle(players_list)
            for i, player_id in enumerate(players_list):
                cursor.execute(f"UPDATE players SET {id_param} = %s WHERE id = %s", (players_list[(i+1)%len(players_list)], player_id))
            conn.commit()

@app.route('/assign', methods=['POST'])
def assign():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM players")
            players = cursor.fetchall()
            if len(players) < 2:
                flash("Il faut au moins deux joueurs pour assigner des cibles.")
                return redirect('/')
            assign_ids(players, "target_id")
            conn.commit()
    return redirect('/8888')

@app.route('/8888')
def admin():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM players ORDER BY username ASC")
            players = cursor.fetchall()
    return render_template('admin.html', players=players)

@app.route('/get_player_id')
def get_player_id():
    username = request.args.get('username')
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT link_id FROM players WHERE username = %s", (username,))
            
            player = cursor.fetchone()
            if player:
                print(player[0])
                return str(player[0])
            else:
                return "Not found", 404

@app.route('/')
def index():
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT username, link_id FROM players ORDER BY username ASC")
            players = cursor.fetchall()
    return render_template('index.html', players=players)

@app.route('/player/<string:link_id>')
def player(link_id):
    with psycopg2.connect(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM players WHERE link_id = %s", (link_id,))
            player = cursor.fetchone()
            if not player:
                flash("Lien invalide.")
                return redirect('/')
            cursor.execute("SELECT * FROM players WHERE id = %s", (player['target_id'],))
            target = cursor.fetchone()
    return render_template('player.html', player=player, target=target)

if __name__ == '__main__':
    # drop_db()
    print('a')
    init_db()
    app.run(debug=True)