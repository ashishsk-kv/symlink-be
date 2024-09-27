from flask import Blueprint, jsonify, request
from app.sessions.model import Sessions
from app.chats.model import Chats
from app.configurations.model import Configurations
from app import db
import hashlib

# Define a blueprint for the routes
sessions = Blueprint('sessions', __name__)

def hash_email(email):
    # Ensure the email is encoded to bytes before hashing
    email_bytes = email.encode('utf-8')
    
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Pass the email bytes to the hash object
    sha256_hash.update(email_bytes)
    
    # Get the hexadecimal digest of the hash
    hashed_email = sha256_hash.hexdigest()
    
    return hashed_email

# Route to create a new user
@sessions.route('/sessions/create', methods=['POST'])
def create_sessions():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    id = None
    session = None
    # Check if the email already exists
    existing_user = Sessions.query.filter_by(email=email).first()
    if existing_user:
        id = existing_user.id
        session = existing_user
    # Create a new user
    else:
        id = hash_email(email=email)
        new_session = Sessions(id=id, email=email)
        db.session.add(new_session)
        db.session.commit()
        session = new_session

    conf = Configurations.query.first()

    chat = Chats(session_id=id, model_name=conf.model_name)
    db.session.add(chat)
    db.session.commit()

    resp = {
        'chat': chat.to_dict(),
        'session': session.to_dict(),
    }

    return jsonify(resp), 201

@sessions.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Sessions.query.all()
    return jsonify([session.to_dict() for session in sessions])