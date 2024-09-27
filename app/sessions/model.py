from app import db

class Sessions(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sensitivity_score = db.Column(db.JSON, nullable=True)
    sesitive_tokens = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<Sessions {self.id}>"

    # Convert object to dictionary (useful for JSON serialization)
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'sensitivity_score': self.sensitivity_score,
            'sesitive_tokens': self.sesitive_tokens
        }
