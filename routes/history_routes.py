from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from modules.report import get_violations
from modules.database import connect

import os

history_bp = Blueprint('history', __name__)


# HISTORY PAGE
@history_bp.route('/history')
def history():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    search = request.args.get('search', '').lower()

    page = request.args.get('page', 1, type=int)

    per_page = 6

    data = get_violations()

    # SEARCH FILTER
    if search:

        data = [
            item for item in data
            if search in item[2].lower()
        ]

    # PAGINATION
    total = len(data)

    start = (page - 1) * per_page
    end = start + per_page

    paginated_data = data[start:end]

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'history.html',
        images=paginated_data,
        page=page,
        total_pages=total_pages,
        search=search
    )


# DELETE RECORD
@history_bp.route('/delete-record/<int:id>')
def delete_record(id):

    if not session.get('logged_in'):

        return redirect(url_for('auth.login'))

    conn = connect()

    cur = conn.cursor()

    # GET IMAGE PATH USING REAL ID
    cur.execute(
        "SELECT image FROM violations WHERE id=?",
        (id,)
    )

    row = cur.fetchone()

    if row:

        image_path = row[0]

        # DELETE IMAGE FILE
        if os.path.exists(image_path):

            os.remove(image_path)

        # DELETE DATABASE RECORD
        cur.execute(
            "DELETE FROM violations WHERE id=?",
            (id,)
        )

        conn.commit()

    conn.close()

    return redirect('/history')