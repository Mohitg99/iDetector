from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from modules.database import connect
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

# LOGIN

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # If already logged in
    if session.get('logged_in'):
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        user = cur.fetchone()

        conn.close()

        # Verify password
        if user and check_password_hash(user[0], password):

            # REMOVE OLD FLASHES
            session.pop('_flashes', None)

            # Session data
            session['logged_in'] = True
            session['user'] = username

            flash("Login successful!", "success")

            return redirect(url_for('dashboard.dashboard'))

        else:

            session.pop('_flashes', None)

            flash("Invalid username or password", "danger")

            return render_template("login.html")

    return render_template("login.html")


# LOGOUT

@auth_bp.route('/logout')
def logout():

    # CLEAR SESSION
    session.clear()

    # REMOVE OLD FLASHES
    session.pop('_flashes', None)

    flash("Logged out successfully!", "success")

    return redirect(url_for('auth.login'))