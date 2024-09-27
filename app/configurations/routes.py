from flask import Blueprint, jsonify, request
from app import db
from app.configurations.model import Configurations

# Define a blueprint for the routes
configurations = Blueprint('configurations', __name__)

# Route to create a new user
@configurations.route('/configurations', methods=['POST'])
def create_sessions():
    data = request.get_json()
    model_name = data.get('model_name')
    key = data.get('secret_key')
    token_size = data.get('token_size')
    temperature = data.get('temperature')
    system_message = data.get('system_message')
    frequency_penalty = data.get('frequency_penalty')

    if not model_name or not key:
        return jsonify({'error': 'model_name and key is required'}), 400

    model = None
    # Check if the email already exists
    existing_model = Configurations.query.filter_by(model_name=model_name).first()
    if existing_model:
        existing_model.secret_key = key
        existing_model.token_size = token_size
        existing_model.temperature = temperature
        existing_model.system_message = system_message
        existing_model.frequency_penalty = frequency_penalty
        model = existing_model
    else:
        # Create a new model
        new_config = Configurations(model_name=model_name, secret_key=key, temperature=temperature, system_message=system_message, frequency_penalty=frequency_penalty)
        db.session.add(new_config)
        model = new_config

    db.session.commit()

    return jsonify(model.to_dict()), 201

@configurations.route('/configurations', methods=['GET'])
def get_sessions():
    configurations = Configurations.query.all()
    return jsonify([configuration.to_dict() for configuration in configurations])