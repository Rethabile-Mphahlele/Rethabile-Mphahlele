import psycopg2

try:
   
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="Maumela@20", host="localhost", port="5432"
    )
    cursor = conn.cursor()

    
    cursor.execute("SELECT first_name, second_name, score FROM scores WHERE score = (SELECT MAX(score) FROM scores) ORDER BY first_name, second_name")

   
    top_scorers = cursor.fetchall()

   
    print("Top Scorers:")
    for scorer in top_scorers:
        print(f"{scorer[0]} {scorer[1]} with a score of {scorer[2]}")

except Exception as e:
    print("Error:", e)

finally:
   
    if conn:
        cursor.close()
        conn.close()
