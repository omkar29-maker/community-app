# 🌍 Community Help App

A simple offline-first web application that connects people who need help with workers looking for opportunities.

## 🚀 Live Demo

https://community-app-3t0o.onrender.com

---

## 💡 Features

* 🔐 User Authentication (Login / Register)
* 📝 Post Job Listings
* 🔎 Browse Available Jobs
* 📱 Mobile-friendly UI
* ⚡ Offline Support (Service Worker)
* 🚨 Emergency Contact Page (Ambulance, Police, Fire)

---

## 🛠️ Tech Stack

* Python (Flask)
* HTML / CSS / JavaScript
* SQLite (Database)
* Gunicorn (Production Server)
* Render (Deployment)

---

## 📦 Project Structure

community_app/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── jobs.html
│   ├── post_job.html
│   ├── login.html
│   ├── register.html
│   └── contacts.html
│
└── static/
├── style.css
├── app.js
└── sw.js

---

## ⚙️ How to Run Locally

git clone https://github.com/omkar29-maker/community-app.git
cd community-app
pip install -r requirements.txt
python3 app.py

Then open:
http://127.0.0.1:5000

---

## 🌱 Future Improvements

* Persistent database (PostgreSQL)
* Location-based job filtering
* Multi-language support
* Admin dashboard
* Real-time notifications

---

## 👨‍💻 Author

Omkar Gore
Passionate about building real-world solutions
