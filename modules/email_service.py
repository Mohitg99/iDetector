import smtplib
from email.message import EmailMessage
from config import Config


def send_email(filepath):

    try:

        msg = EmailMessage()

        msg['Subject'] = "iDetector Report"
        msg['From'] = Config.EMAIL
        msg['To'] = Config.EMAIL

        msg.set_content(
            "Attached is your iDetector AI Detection Report."
        )

        with open(filepath, 'rb') as f:

            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='pdf',
                filename='report.pdf'
            )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

            smtp.login(Config.EMAIL, Config.PASSWORD)

            smtp.send_message(msg)

        return True

    except Exception as e:

        print("EMAIL ERROR:", e)

        return False