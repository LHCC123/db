from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

USERS_FILE = 'users.json'

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([{"username": "god", "password": "god123", "role": "god"}], f, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/users', methods=['GET'])
def get_users():
    with open(USERS_FILE, 'r') as f:
        return jsonify(json.load(f))

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    if any(u['username'] == username for u in users):
        return jsonify({"error": "Usuario ya existe"}), 400

    users.append({"username": username, "password": password, "role": role})

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

    return jsonify({"message": f"Usuario '{username}' creado correctamente"})

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    username = data.get('username', '').lower()

    if username == "god":
        return jsonify({"error": "No puedes eliminar al usuario God"}), 400

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    users = [u for u in users if u['username'] != username]

    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

    return jsonify({"message": f"Usuario '{username}' eliminado"})

# ==================== REGISTROS ====================
REGISTROS_FILE = 'registros.json'

if not os.path.exists(REGISTROS_FILE):
    with open(REGISTROS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/registros', methods=['GET'])
def get_registros():
    with open(REGISTROS_FILE, 'r') as f:
        return jsonify(json.load(f))

@app.route('/save_registros', methods=['POST'])
def save_registros():
    data = request.json
    with open(REGISTROS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({"message": "Registros guardados correctamente"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

