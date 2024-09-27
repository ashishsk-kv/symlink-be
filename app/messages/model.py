from app import db
from datetime import datetime

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, db.Sequence('seq_message_id', start=1, increment=1), primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    send_date = db.Column(db.DateTime, default=datetime.now)
    direction = db.Column(db.String, nullable=False)
    sent_by = db.Column(db.String, nullable=False)
    documents = db.Column(db.JSON, nullable=True)
    masked_content = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Messages {self.id}>"

    # Convert object to dictionary (useful for JSON serialization)
    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'content': self.content,
            'send_date': self.send_date.strftime('%Y-%m-%d %H:%M:%S'),
            'sent_by': self.sent_by,
            'documents': self.documents,
            'masked_content': self.masked_content
        }
