import psycopg2


DB_NAME = "test_scores"
DB_USER = "postgres"  
DB_PASSWORD = "Maumela@20"  
DB_HOST = "localhost"
DB_PORT = "5432"


data = [
    ("Dee", "Moore", 56),
    ("Sipho", "Lolo", 78),
    ("Noosrat", "Hoosain", 64),
    ("George", "Of The Jungle", 78)
]

try:
    
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    
    insert_query = "INSERT INTO scores (first_name, second_name, score) VALUES (%s, %s, %s)"
    cur.executemany(insert_query, data)

    
    conn.commit()

    print("Data inserted successfully!")

   
    cur.close()
    conn.close()
except Exception as e:
    print("Error inserting data:", e)
