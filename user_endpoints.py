from flask import Flask, request, jsonify
from user import User  # Import the User class from user.py

app = Flask(__name__)

@app.route('/')
def home():
    message = 'Welcome my little Holbitch'
    return message

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User.create(data)
    return jsonify(user.to_dict()), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.read(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.update(user_id, data)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.delete(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
