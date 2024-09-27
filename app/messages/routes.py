from flask import Blueprint, jsonify
from app.messages.model import Messages
from app import db, socketio
from flask_socketio import emit
from app.sessions.model import Sessions
from app.chats.model import Chats
from app.ner.ner_prediction import get_prediction
from app.utils import map_keys, reverse_map
from app.llms import openai_util

# Define a blueprint for the routes
messages = Blueprint('messages', __name__)

@messages.route('/messages/<chat_id>', methods=['GET'])
def get_sessions(chat_id):
    if not chat_id:
        return jsonify({'error': 'Chat Id is required'}), 400
    messages = Messages.query.filter_by(chat_id=chat_id).all()
    return jsonify([message.to_dict() for message in messages])

@socketio.on('send_message')
def handle_send_message(data):
    print(f"Message received: {data.get('message')}")
    session_id = data.get('session_id')
    message_text = data.get('message')
    chat_id = data.get('chat_id')
    model_name = data.get('model_name')

    if not session_id or not message_text:
        return emit('error', {'error': 'Invalid data'})

    # Get the user and room from the database
    user = Sessions.query.filter_by(id=session_id).first()

    if not chat_id:
        chat = Chats(session_id=user.id, model_name=model_name, title=message_text[:20])
    else:
        chat = Chats.query.filter_by(id=chat_id).first()
        if not chat:
            chat = Chats(session_id=user.id, model_name=model_name, title=message_text[:20])
    db.session.add(chat)
    db.session.commit()
    
    print(f"Chat created with id: {chat.id}")

    if not user or not chat:
        return emit('error', {'error': 'Invalid user or chat'})

    # Create the message in the database
    message = Messages(chat_id=chat.id, content=message_text, direction='SENT', sent_by=user.id)
    masked_text, mapped_entity = get_prediction(message_text)
    message.masked_content = masked_text
    db.session.add(message)
    db.session.commit()

    emit('receive_message', message.to_dict(), broadcast=True)
    
    entity_key_map = map_keys(mapped_entity)

    gpt_response = openai_util.query_chatgpt(masked_text)

    final_output = reverse_map(gpt_response, entity_key_map)

    reply = Messages(chat_id=chat.id, content=final_output, direction='RECEIVED', sent_by='MODEL')
    db.session.add(reply)
    db.session.commit()

    # Broadcast the message to the room
    emit('receive_message', reply.to_dict(), broadcast=True)
    

@socketio.on('get_history')
def get_chat_history(data):
    chat_id = data.get('chat_id')
    session_id = data.get('session_id')

    if not session_id or not chat_id:
        return emit('error', {'error': 'Invalid data'})
    
    user = Sessions.query.filter_by(id=session_id).first()
    chat = Chats.query.filter_by(id=chat_id).first()

    if not chat or not user:
        return emit('error', {'error': 'Invalid user or chat'})
    
    messages = Messages.query.filter_by(chat_id=chat.id).all()
    formatted_messages = [message.to_dict() for message in messages]

    emit('chat_history', formatted_messages, broadcast=True) 