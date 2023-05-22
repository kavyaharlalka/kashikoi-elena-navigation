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


def test_insert_into_database_invalid_data():
    source = 'Dummy source'
    destination = 'Dummy destination'
    algorithm_id = 10
    path_percent = 200
    minimize_elevation_gain = True
    transportation_mode = 1
    json_result = {'testingKeyStr': 'testingValue', 'testingKeyInt': 10, 'testingKeyBool': True}

    with pytest.raises(IntegrityError, match='CHECK constraint failed: history'):
        db_manager.insert_into_database(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, json_result)


