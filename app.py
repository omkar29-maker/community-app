from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"  # needed for login

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Jobs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            location TEXT,
            contact TEXT,
            salary TEXT,
            workers TEXT,
            meals TEXT,
            description TEXT
        )
    ''')

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    data = c.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=data)

@app.route('/post', methods=['GET', 'POST'])
def post_job():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        contact = request.form['contact']
        salary = request.form['salary']
        workers = request.form['workers']
        meals = request.form['meals']
        description = request.form['description']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
        INSERT INTO jobs (title, location, contact, salary, workers, meals, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, location, contact, salary, workers, meals, description))

        conn.commit()
        conn.close()

        return redirect('/jobs')

    return render_template('post_job.html')

# 🔐 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid login"

    return render_template('login.html')

# 🔐 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)