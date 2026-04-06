from flask import Flask, render_template, request, redirect, session
import os
import psycopg2

app = Flask(__name__)
app.secret_key = "secret123"

# 🔗 Connect to PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 🛠️ Create tables
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

# 🌐 LANGUAGE SYSTEM
translations = {
    "en": {
        "title": "Community Help App",
        "welcome_login": "Welcome back! Keep going, you are doing great 💪",
        "welcome_register": "Welcome! Your journey starts here 🚀"
    },
    "hi": {
        "title": "समुदाय सहायता ऐप",
        "welcome_login": "वापसी पर स्वागत है! आप बहुत अच्छा कर रहे हैं 💪",
        "welcome_register": "स्वागत है! आपकी यात्रा यहीं से शुरू होती है 🚀"
    },
    "mr": {
        "title": "समुदाय मदत अ‍ॅप",
        "welcome_login": "पुन्हा स्वागत आहे! तुम्ही खूप छान करत आहात 💪",
        "welcome_register": "स्वागत आहे! तुमचा प्रवास इथून सुरू होतो 🚀"
    },
    "kr": {
        "title": "커뮤니티 도움 앱",
        "welcome_login": "다시 오신 것을 환영합니다! 잘하고 있어요 💪",
        "welcome_register": "환영합니다! 당신의 여정이 시작됩니다 🚀"
    }
}

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect('/')

def get_lang():
    return session.get('lang', 'en')

# 🏠 Home
@app.route('/')
def index():
    lang = get_lang()
    t = translations.get(lang, translations['en'])
    message = session.pop('message', None)
    return render_template('index.html', t=t, message=message)

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

        lang = get_lang()
        t = translations.get(lang, translations['en'])
        session['message'] = t['welcome_register']

        return redirect('/')

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

            lang = get_lang()
            t = translations.get(lang, translations['en'])
            session['message'] = t['welcome_login']

            return redirect('/')
        else:
            return "Invalid login"

    return render_template('login.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# 📞 Contacts
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)
