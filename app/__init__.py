from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

# Initialize the database
db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('app.config.Config')
    
    # Initialize the database with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    socketio.init_app(app, cors_allowed_origins="*")

    @app.route('/')
    def get_index():
        return render_template("index.html")

    return app
