from flask import Blueprint, jsonify, request
from app.chats.model import Chats

# Define a blueprint for the routes
chats = Blueprint('chats', __name__)

@chats.route('/chats', methods=['GET'])
def get_chats():
    session_id = request.args.get('session_id')
    chats = Chats.query.filter_by(session_id=session_id).all()
    return jsonify([chat.to_dict() for chat in chats])