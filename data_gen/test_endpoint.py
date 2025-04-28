from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    # Get JSON data from the request.
    data = request.get_json()

    # Print received data.
    print("Received data:", data)

    # Send success message.
    return jsonify({"message": "Data received successfully", "data_count": len(data)}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
