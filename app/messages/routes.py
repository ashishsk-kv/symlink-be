from flask import Blueprint, jsonify, request
from app.messages.model import Messages
from app import db, socketio
from flask_socketio import emit
from app.sessions.model import Sessions
from app.chats.model import Chats
from app.ner.ner_prediction import get_prediction
from app.utils import map_keys, reverse_map, clean_white_space, mask_user_message, reverse_map_gpt_resp
from app.llms import openai_util
from app.ocr.routes import extract_text
from app.model import model_util
import os, json
from re import findall
from app.config import demo_type
from string import ascii_uppercase

# Define a blueprint for the routes
messages = Blueprint('messages', __name__)

@messages.route('/messages/<chat_id>', methods=['GET'])
def get_sessions(chat_id):
    if not chat_id:
        return jsonify({'error': 'Chat Id is required'}), 400
    messages = Messages.query.filter_by(chat_id=chat_id).all()
    return jsonify([message.to_dict() for message in messages])

@messages.route('/messages/review_message', methods=['POST'])
def review_message():
    data = request.get_json()
    session_id = data.get('session_id')
    message_text = data.get('message')
    chat_id = data.get('chat_id')
    model_name = data.get('model_name')

    if not message_text:
        return jsonify({'error': 'original message is required'}), 400
    
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
    
    message = Messages(chat_id=chat.id, content=message_text, direction='SENT', sent_by=user.id)
    masked_text, mapped_entity = get_prediction(message_text)
    message.masked_content = masked_text
    db.session.add(message)
    db.session.commit()
    res = {
        'message': message_text, 
        'masked_text': masked_text, 
        'mapped_entity': mapped_entity,
        'message_id': message.id,
        'chat_id': chat.id
    }
    # emit('receive_message', res, broadcast=True)
    return jsonify(res), 201

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
    db.session.add(message)
    db.session.commit()

    emit('receive_message', message.to_dict(), broadcast=True)
    # masked_text, mapped_entity = get_prediction(message_text)
    response = model_util.query(message_text)
    print("raw response-:", response)
    if demo_type == "PII-IDENTIFICATION":
        pattern = r"'([^']+)'"
        matches = findall(pattern, clean_white_space(response))
        entity_details = {f"ENTITY_{alpha_id}": match for match, alpha_id in  zip(matches, list(ascii_uppercase))}
    else:
        json_response =  json.loads(response)
        entity_details = {value: key for key, value in json_response.items()}

    emit('receive_message', message.to_dict(), broadcast=True)

    masked_text = mask_user_message(message_text, entity_details)
    print("masked_text", masked_text) # PR_DELETE
    created_message = Messages.query.filter_by(id=message.id).first()
    created_message.masked_content = masked_text
    db.session.commit()
    gpt_response = openai_util.query_chatgpt(masked_text)
    final_output = reverse_map_gpt_resp(gpt_response, entity_details)

    reply = Messages(chat_id=chat.id, content=final_output, direction='RECEIVED', sent_by='MODEL')
    db.session.add(reply)
    db.session.commit()

    # Broadcast the message to the room
    emit('receive_message', reply.to_dict(), broadcast=True)


@socketio.on('send_message_with_file')
def handle_send_message(data):
    print(f"Message received with file: {data.get('message')}")
    session_id = data.get('session_id')
    message_text = data.get('message')
    chat_id = data.get('chat_id')
    model_name = data.get('model_name')
    filename = data.get('filename')
    file = data.get('file')

    if not session_id or (not message_text and not file):
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

    if file:
        # Saving the file
        with open(os.path.join('uploads/', filename), 'wb') as f:
            f.write(file)
    
    print(f"Chat created with id: {chat.id}")

    if not user or not chat:
        return emit('error', {'error': 'Invalid user or chat'})

    # Create the message in the database
    message = Messages(chat_id=chat.id, content=message_text, direction='SENT', sent_by=user.id, documents=['uploads/'+str(filename)])
    extracted_text = extract_text(filepath='uploads/'+str(filename))['extracted_text']
    masked_text, mapped_entity = get_prediction(extracted_text)
    message.masked_content = masked_text
    db.session.add(message)
    db.session.commit()

    res = {
        'message': extracted_text,
        'masked_text': masked_text, 
        'mapped_entity': mapped_entity,
        'message_id': message.id,
        'chat_id': chat.id
    }

    emit('review_file', res, broadcast=True)


@socketio.on('review_message')
def review_message(data):
    print(f"Message received: {json.dumps(data)}")
    session_id = data.get('session_id')
    message_text = data.get('message')
    entity_map = data.get('entity_map')
    message_id = data.get('message_id')
    chat_id = data.get('chat_id')

    if not session_id or not message_text:
        return emit('error', {'error': 'Invalid data'})

    # Get the user and room from the database
    user = Sessions.query.filter_by(id=session_id).first()
    chat = Chats.query.filter_by(id=chat_id).first()

    if not user or not chat:
        return emit('error', {'error': 'Invalid user or chat'})

    # Create the message in the database
    message = Messages.query.filter_by(id=message_id).first()
    # masked_text, mapped_entity = get_prediction(message_text)
    message.masked_content = message_text
    db.session.commit()

    emit('receive_message', message.to_dict(), broadcast=True)

    gpt_response = openai_util.query_chatgpt(message_text)

    final_output = reverse_map(gpt_response, entity_map)

    reply = Messages(chat_id=chat.id, content=final_output, direction='RECEIVED', sent_by='MODEL')
    db.session.add(reply)
    db.session.commit()

    # Broadcast the message to the room
    emit('receive_message', reply.to_dict(), broadcast=True)
    

@socketio.on('get_history')
def get_chat_history(data):
    print(f"Get history message received: {json.dumps(data)}")
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

    print(f"Formatted messages: {json.dumps(formatted_messages)}")

    emit('chat_history', formatted_messages, broadcast=True) 
