import sqlite3
import config
class SQL:
    def __init__(self):
        self.table_name = config.TABLE_NAME
        self.conn = sqlite3.connect(config.DATABASE_NAME)
        print("Successfully connected to Database")
        self.conn.execute('DROP TABLE history')
        self.conn.execute(f'''CREATE TABLE {self.table_name}
                 (source TEXT NOT NULL,
                 destination TEXT NOT NULL,
                 algorithm_id INT NOT NULL CHECK (algorithm_id BETWEEN 0 AND 6),
                 path_percent INT NOT NULL CHECK (path_percent BETWEEN 100 AND 200),
                 minimize_elevation_gain BOOLEAN NOT NULL CHECK (minimize_elevation_gain IN (0, 1)),
                 transportation_mode TEXT NOT NULL);''')


    def insert_into_database(self, source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode):
        print(algorithm_id)
        self.conn.execute(f'INSERT INTO {self.table_name} (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode) VALUES (?,?,?,?,?,?);', (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode))

    def get_navigation_if_exists(self, source, destination, algorithm_id):
        result = self.conn.execute(f'select * from {self.table_name} where source = ? and destination = ? and algorithm_id = ?;', (source, destination, algorithm_id))
        # fetch() needed?
        return result

    def close_database_connection(self):
        res = self.conn.execute("SELECT * FROM history")
        print(res.fetchall())
        self.conn.close()



if __name__ == "__main__":
    sql = SQL()
    sql.insert_into_database("UMass", "Brandywine", 6, 110, 0, "bike")
    sql.get_navigation_if_exists("UMass", "Brandywine", 6)
    sql.close_database_connection()
