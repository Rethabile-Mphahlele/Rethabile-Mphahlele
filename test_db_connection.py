import psycopg2


DB_NAME = "test_scores"
DB_USER = "postgres"  
DB_PASSWORD = "Maumela@20"  
DB_HOST = "localhost"
DB_PORT = "5432" 

try:
    
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    print("Successfully connected to PostgreSQL!") 

    
    conn.close()
except Exception as e:
    print("Connection failed:", e)  

