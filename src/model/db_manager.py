import sqlite3
import config

table_name = config.TABLE_NAME

conn = sqlite3.connect(config.DATABASE_NAME)
print("Successfully connected to Database")

conn.execute(f'''CREATE TABLE {table_name}
         (id INT PRIMARY KEY NOT NULL,
         source TEXT NOT NULL,
         destination INT NOT NULL,
         algorithm CHAR(50),
         path REAL);''')

def insert_into_database(source, destination, algorithm, path):
    conn.execute(f'INSERT INTO {table_name} VALUES ?;', (source, destination, algorithm, path))

def get_navigation_if_exists(source, destination, algorithm):
    result = conn.execute(f'select path from {table_name} where source = ? and destination = ? and algorithm = ?;', (source, destination, algorithm))
    # fetch() needed?
    return result

def close_database_connection():
    conn.close()