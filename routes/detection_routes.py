from flask import (
    Blueprint,
    Response,
    render_template,
    session,
    redirect,
    url_for,
    jsonify
)

from modules.detection import (
    generate_frames,
    live_face_count,
    live_violation_count
)

detection_bp = Blueprint('detect', __name__)


# WEBCAM PAGE
@detection_bp.route('/webcam')
def webcam():

    # Protect webcam route
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    return render_template("webcam.html")


# VIDEO FEED
@detection_bp.route('/video_feed')
def video_feed():

    # Protect video stream
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# LIVE STATS API
@detection_bp.route('/live-stats')
def live_stats():

    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    return jsonify({
        "faces": live_face_count,
        "violations": live_violation_count
    })