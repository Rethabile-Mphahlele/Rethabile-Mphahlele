from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        dbname="test_db", user="postgres", password="Maumela@20", host="localhost", port="5432"
    )


def parse_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:  
            values = line.strip().split(',')  
            if len(values) == 3:  
                first_name, second_name, score = values[0], values[1], int(values[2])
                data.append((first_name, second_name, score))
    return data


def insert_csv_to_db(csv_file):
    data = parse_csv(csv_file)
    conn = get_db_connection()
    cursor = conn.cursor()

    for row in data:
        cursor.execute("INSERT INTO scores (first_name, second_name, score) VALUES (%s, %s, %s)", row)

    conn.commit()
    cursor.close()
    conn.close()

# POST: Add a new score
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

    cursor.execute("SELECT first_name, second_name, score FROM scores WHERE score = (SELECT MAX(score) FROM scores) ORDER BY first_name, second_name")
    top_scorers = cursor.fetchall()

    cursor.close()
    conn.close()

    if top_scorers:
        return jsonify([{"first_name": scorer[0], "second_name": scorer[1], "score": scorer[2]} for scorer in top_scorers])
    else:
        return jsonify({"message": "No top scorers found"}), 404


if __name__ == '__main__':
   
    insert_csv_to_db("TestData.csv")  
    print("CSV data has been inserted into the database!")

    app.run(debug=True)
