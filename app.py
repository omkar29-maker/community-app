from flask import Flask, render_template, request, redirect, session
import os
import psycopg2

app = Flask(__name__)
app.secret_key = "secret123"

# 🔗 Connect to PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 🛠️ Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    location TEXT,
    contact TEXT,
    salary TEXT,
    workers TEXT,
    meals TEXT,
    description TEXT
);
""")

conn.commit()

# 🏠 Home
@app.route('/')
def index():
    return render_template('index.html')

# 📋 View Jobs
@app.route('/jobs')
def jobs():
    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template('jobs.html', jobs=data)

# ➕ Post Job
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

        cursor.execute("""
        INSERT INTO jobs (title, location, contact, salary, workers, meals, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, location, contact, salary, workers, meals, description))

        conn.commit()
        return redirect('/jobs')

    return render_template('post_job.html')

# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        """, (username, password))

        conn.commit()
        return redirect('/login')

    return render_template('register.html')

# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("""
        SELECT * FROM users WHERE username=%s AND password=%s
        """, (username, password))

        user = cursor.fetchone()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid login"

    return render_template('login.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# 📞 Contacts page
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)
