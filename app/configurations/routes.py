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

    if not model_name or not key:
        return jsonify({'error': 'model_name and key is required'}), 400

    # Check if the email already exists
    existing_model = Configurations.query.filter_by(model_name=model_name).first()
    if existing_model:
        return jsonify({'error': 'Model already exists'}), 400

    # Create a new model
    new_config = Configurations(model_name=model_name, secret_key=key)
    db.session.add(new_config)
    db.session.commit()

    return jsonify(new_config.to_dict()), 201

@configurations.route('/configurations', methods=['GET'])
def get_sessions():
    configurations = Configurations.query.all()
    return jsonify([configuration.to_dict() for configuration in configurations])