from werkzeug.security import generate_password_hash, check_password_hash
from modules.database import connect

def register_user(username, password):
    conn = connect()
    cur = conn.cursor()

    hashed = generate_password_hash(password)

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))

    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user[0], password):
        return True

    return False