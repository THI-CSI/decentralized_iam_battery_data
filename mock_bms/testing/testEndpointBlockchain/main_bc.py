from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

# Define the path to the did.json file
CLOUD_JSON_PATH = 'cloud.json'

@app.route('/api/dids/did:batterypass:896ad506-9843-48d3-b599-be45fca2bb3e', methods=['GET'])
def get_did():
    # Check if the did.json file exists
    if os.path.exists(CLOUD_JSON_PATH):
        return send_file(CLOUD_JSON_PATH, mimetype='application/json')
    else:
        return jsonify({"error": "cloud.json not found"}), 404

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
