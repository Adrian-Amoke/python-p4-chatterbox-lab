from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        if messages:
            messages_serialized = [message.to_dict() for message in messages]
            return make_response(jsonify(messages_serialized), 200)
        else:
            return make_response(jsonify({'error': 'No messages found'}), 404)
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)
    

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = Message.query.get(id)
        if message:
            data = request.get_json()
            for key, value in data.items():
                setattr(message, key, value)
            db.session.commit()
            return make_response(jsonify(message.to_dict()), 200)
        else:
            return make_response(jsonify({'error': 'Message not found'}), 404)
    elif request.method == 'DELETE':
        message = Message.query.get(id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return make_response(jsonify({'message': 'Message deleted'}), 200)
        else:
            return make_response(jsonify({'error': 'Message not found'}), 404)

if __name__ == '__main__':
    app.run(port=5555)
