import json
from sqlite3 import IntegrityError

import src.model.db_manager as db_manager
import pytest
import sqlite3
import src.config as config


def cleanup_delete_record(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode):
    connection = sqlite3.connect(config.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(f'delete from {config.TABLE_NAME} where source = ? and destination = ? and algorithm_id = ? and path_percent = ? and minimize_elevation_gain = ? and transportation_mode = ?;',
                          (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode))
    connection.commit()
    cursor.close()
    connection.close()



