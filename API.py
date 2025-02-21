from flask import Flask, request, jsonify, abort

app = Flask(__name__)


VALID_API_KEYS = {
    "my-secret-api-key": "Maumela",
    "another-api-key": "User"
}


def check_api_key():
    api_key = request.headers.get("API-Key")
    if api_key not in VALID_API_KEYS:
        abort(403, description="Forbidden: Invalid API Key")
    return VALID_API_KEYS[api_key]  

@app.route('/scores', methods=['POST'])
def add_score():
    
    user = check_api_key()

    
    data = request.get_json()
    first_name = data.get('first_name')
    second_name = data.get('second_name')
    score = data.get('score')

   

    return jsonify({"message": f"Score added successfully by {user}!"}), 201

@app.route('/top_scorers', methods=['GET'])
def get_top_scorers():
    
    user = check_api_key()

   

    return jsonify([{"first_name": scorer[0], "second_name": scorer[1], "score": scorer[2]} for scorer in top_scorers])

if __name__ == '__main__':
    app.run(debug=True)
