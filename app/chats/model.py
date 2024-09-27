from app import db
from datetime import datetime

class Chats(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, db.Sequence('seq_chat_id', start=1, increment=1), primary_key=True)
    title = db.Column(db.String, nullable=False)
    session_id = db.Column(db.String, db.ForeignKey('sessions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    model_name = db.Column(db.String, db.ForeignKey('configurations.model_name'), nullable=False)

    def __repr__(self):
        return f"<Chats {self.id}>"

    # Convert object to dictionary (useful for JSON serialization)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'session_id': self.session_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'model_name': self.model_name
        }
