from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        nation TEXT,
        role TEXT,
        avg REAL,
        sr REAL,
        matches INTEGER,
        runs INTEGER
    )
''')


    # Ensure all columns exist (safe for previously created tables)
    try:
        c.execute("ALTER TABLE players ADD COLUMN team TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE players ADD COLUMN nation TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE players ADD COLUMN role TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE players ADD COLUMN avg INTEGER")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE players ADD COLUMN sr INTEGER")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE players ADD COLUMN matches INTEGER")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE players ADD COLUMN runs INTEGER")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute("SELECT name, nation, role, avg, sr, matches, runs FROM players")
    players = c.fetchall()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    nation = request.form['nation']
    role = request.form['role']
    avg = request.form['avg']
    sr = request.form['sr']
    matches = request.form['matches']
    runs = request.form['runs']

    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('INSERT INTO players (name, nation, role, avg, sr, matches, runs) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (name, nation, role, avg, sr, matches, runs))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
