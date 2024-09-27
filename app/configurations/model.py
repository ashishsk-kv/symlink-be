from app import db

class Configurations(db.Model):
    __tablename__ = 'configurations'

    model_name = db.Column(db.String, primary_key=True)
    secret_key = db.Column(db.String, nullable=False)
    token_size = db.Column(db.Integer, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    system_message = db.Column(db.String, nullable=True)
    frequency_penalty = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Configurations {self.model_name}>"

    # Convert object to dictionary (useful for JSON serialization)
    def to_dict(self):
        return {
            'model_name': self.model_name,
            'secret_key': self.secret_key,
            'token_size': self.token_size,
            'temperature': self.temperature,
            'system_message': self.system_message,
            'frequency_penalty': self.frequency_penalty
        }
