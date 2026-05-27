from flask import Flask
from config import Config
from modules.database import create_tables
import os
from routes.history_routes import history_bp
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.detection_routes import detection_bp
from routes.report_routes import report_bp

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs("instance", exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    create_tables()

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(report_bp)
    return app

app = create_app()
app.register_blueprint(history_bp)

if __name__ == "__main__":
    app.run(debug=True)