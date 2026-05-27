from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify
)

from modules.report import (
    get_violations,
    get_filtered_violations,
    get_violation_stats,
    get_chart_data
)

dashboard_bp = Blueprint('dashboard', __name__)

# DASHBOARD

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    # Protect dashboard
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    # Filter data
    if request.method == 'POST':

        start = request.form.get('start')
        end = request.form.get('end')

        images = get_filtered_violations(start, end)

    else:

        images = get_violations()

    total = len(images)

    stats = get_violation_stats()

    result_data, daily_data = get_chart_data()

    return render_template(
        "dashboard.html",
        images=images,
        total=total,
        stats=stats,
        result_data=result_data,
        daily_data=daily_data
    )

# LIVE DASHBOARD API

@dashboard_bp.route('/api/dashboard-data')
def dashboard_data():

    # API protection
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    images = get_violations()

    stats = get_violation_stats()

    result_data, daily_data = get_chart_data()

    return jsonify({
        "images": images,
        "stats": stats,
        "result_data": result_data,
        "daily_data": daily_data
    })