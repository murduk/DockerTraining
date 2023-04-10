
import psycopg2
import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST") or 'localhost'
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or 'example'
POSTGRES_USER = os.getenv("POSTGRES_USER") or 'postgres'
POSTGRES_DEFAULT_DATABASE = os.getenv("POSTGRES_DEFAULT_DATABASE") or 'postgres'
POST_TABLE_NAME = os.getenv("POST_TABLE_NAME") or 'post'
POST_DB_NAME = os.getenv("POST_DB_NAME") or 'postdb'

def connect_to_database(host, db_name, user, password):
    conn = psycopg2.connect(f"dbname={db_name} user={user} password={password} host={host}")
    conn.autocommit = True
    return conn

def create_database(conn, db_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    if not exists:
      cursor.execute(f'CREATE DATABASE {db_name}')
      print(f'database {db_name} created')
    else:
      print(f'database {db_name} exits')
    cursor.close()
    conn.close()

def create_table(conn, table_name=POST_TABLE_NAME):
   cursor = conn.cursor()
   cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, post VARCHAR(500))")
   cursor.close()
   conn.close()

def insert_post(post, host=POSTGRES_HOST, post_db_name=POST_DB_NAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD):
   conn = connect_to_database(host, post_db_name, user, password)
   cursor = conn.cursor()
   cursor.execute(f"INSERT INTO {POST_TABLE_NAME} (post) VALUES('{post}') RETURNING id")
   id = cursor.fetchone()[0]
   print(f'post created, post id: {id}')
   cursor.close()
   conn.close()

def init_post_database(host=POSTGRES_HOST, post_db_name=POST_DB_NAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD):
    conn = connect_to_database(host, POSTGRES_DEFAULT_DATABASE, user, password)
    create_database(conn, post_db_name)
    conn = connect_to_database(host, post_db_name, user, password)
    create_table(conn)

def get_posts(host=POSTGRES_HOST, post_db_name=POST_DB_NAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD):
    conn = connect_to_database(host, post_db_name, user, password)
    cursor = conn.cursor()
    cursor.execute(f"SELECT post FROM {POST_TABLE_NAME}")
    posts = cursor.fetchall()    
    result = []
    for post in posts:       
       result.append(post[0])    
    return result

if __name__ == "__main__":
    #testing
    init_post_database()
    #insert_post('hello')
    get_posts()

