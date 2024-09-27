from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS

# Initialize the database
db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    CORS(app) # This will enable CORS for all routes

    # Load configuration from config.py
    app.config.from_object('app.config.Config')
    
    # Initialize the database with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Import and register the routes (blueprints)
    from app.sessions.routes import sessions as sessions_blueprint
    app.register_blueprint(sessions_blueprint)

    from app.chats.routes import chats as chats_blueprint
    app.register_blueprint(chats_blueprint)

    from app.configurations.routes import configurations as configurations_blueprint
    app.register_blueprint(configurations_blueprint)

    from app.messages.routes import messages as messages_blueprint
    app.register_blueprint(messages_blueprint)

    from app.ocr.routes import ocr as ocr_blueprint
    app.register_blueprint(ocr_blueprint)

    @app.route('/')
    def get_index():
        return render_template("index.html")

    return app