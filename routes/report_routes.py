from flask import Blueprint, redirect, url_for, flash, send_file, session
from modules.report_pdf import generate_pdf
from modules.email_service import send_email
import csv
from flask import make_response
from modules.database import get_all_detections

report_bp = Blueprint('report', __name__)


# DOWNLOAD PDF REPORT
@report_bp.route('/download-report')
def download_report():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    filepath = generate_pdf()

    return send_file(filepath, as_attachment=True)


# SEND EMAIL REPORT
@report_bp.route('/send-email')
def send_email_route():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    try:

        filepath = generate_pdf()

        success = send_email(filepath)

        if success:
            flash("Email sent successfully!", "success")
        else:
            flash("Failed to send email.", "danger")

    except Exception as e:

        print("EMAIL ERROR:", e)

        flash("Email service error occurred.", "danger")

    return redirect(url_for('dashboard.dashboard'))

@report_bp.route('/export-csv')
def export_csv():

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    data = get_all_detections()

    output = []

    # CSV Header
    output.append("Image,Result,Confidence,Time\n")

    # CSV Rows
    for row in data:

        line = f"{row[0]},{row[1]},{row[2]},{row[3]}\n"

        output.append(line)

    response = make_response("".join(output))

    response.headers["Content-Disposition"] = \
        "attachment; filename=report.csv"

    response.headers["Content-type"] = "text/csv"

    return response