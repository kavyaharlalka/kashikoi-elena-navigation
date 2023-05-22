import sqlite3
import config
import json

table_name = config.TABLE_NAME

connection = sqlite3.connect(config.DATABASE_NAME)
cursor = connection.cursor()
print("Successfully connected to Database")
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
         (source TEXT NOT NULL,
         destination TEXT NOT NULL,
         algorithm_id INT NOT NULL CHECK (algorithm_id BETWEEN 0 AND 5),
         path_percent INT NOT NULL CHECK (path_percent BETWEEN 100 AND 500),
         minimize_elevation_gain BOOLEAN NOT NULL CHECK (minimize_elevation_gain IN (0, 1)),
         transportation_mode INT NOT NULL CHECK (transportation_mode IN (0, 1)),
         result TEXT NOT NULL);''')
connection.commit()
connection.close()

def insert_into_database(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, json_result):
    print(algorithm_id)
    connection = sqlite3.connect(config.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO {table_name} (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, result) VALUES (?,?,?,?,?,?,?);',
                 (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, json.dumps(json_result)))
    connection.commit()
    cursor.close()
    connection.close()

def get_navigation_if_exists(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode):
    connection = sqlite3.connect(config.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f'select result from {table_name} where source = ? and destination = ? and algorithm_id = ? and path_percent = ? and minimize_elevation_gain = ? and transportation_mode = ?;',
                          (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result is not None and len(result) > 0:
        return json.loads(result[0])
    return None