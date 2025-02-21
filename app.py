from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="Maumela@20", host="localhost", port="5432"
    )
    return conn


@app.route('/')
def home():
    return "Welcome to the Top Scorers API!"


@app.route('/scores', methods=['POST'])
def add_score():
    data = request.get_json()  
    first_name = data.get('first_name')
    second_name = data.get('second_name')
    score = data.get('score')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    
    cursor.execute("INSERT INTO scores (first_name, second_name, score) VALUES (%s, %s, %s)",
                   (first_name, second_name, score))
    conn.commit()  
    
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Score added successfully!"}), 201


@app.route('/scores/<first_name>/<second_name>', methods=['GET'])
def get_score(first_name, second_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
  
    cursor.execute("SELECT first_name, second_name, score FROM scores WHERE first_name = %s AND second_name = %s",
                   (first_name, second_name))
    result = cursor.fetchone()  
    
    cursor.close()
    conn.close()
    
    if result:
        return jsonify({"first_name": result[0], "second_name": result[1], "score": result[2]})
    else:
        return jsonify({"message": "Person not found"}), 404


@app.route('/top_scorers', methods=['GET'])
def get_top_scorers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Retrieve the highest score(s)
    cursor.execute("SELECT first_name, second_name, score FROM scores WHERE score = (SELECT MAX(score) FROM scores) ORDER BY first_name, second_name")
    top_scorers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if top_scorers:
        return jsonify([{"first_name": scorer[0], "second_name": scorer[1], "score": scorer[2]} for scorer in top_scorers])
    else:
        return jsonify({"message": "No top scorers found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
