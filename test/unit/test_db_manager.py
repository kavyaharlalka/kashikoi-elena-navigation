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


def test_insert_into_database():
    expected_output_number_of_records = 1

    source = 'Dummy source'
    destination = 'Dummy destination'
    algorithm_id = 0
    path_percent = 200
    minimize_elevation_gain = True
    transportation_mode = 1
    json_result = {'testingKeyStr': 'testingValue', 'testingKeyInt': 10, 'testingKeyBool': True}

    # In case there are old testing records in the database
    cleanup_delete_record(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode)

    db_manager.insert_into_database(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, json_result)

    connection = sqlite3.connect(config.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(
        f'select result from {config.TABLE_NAME} where source = ? and destination = ? and algorithm_id = ? and path_percent = ? and minimize_elevation_gain = ? and transportation_mode = ?;',
        (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode))
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    assert len(result) == expected_output_number_of_records
    assert json.loads(result[0][0]) == json_result

    # Cleanup added record
    cleanup_delete_record(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode)


def test_get_navigation_if_exists():
    expected_output = {'testingKeyStr': 'testingValue', 'testingKeyInt': 10, 'testingKeyBool': True}

    source = 'Dummy source'
    destination = 'Dummy destination'
    algorithm_id = 0
    path_percent = 200
    minimize_elevation_gain = True
    transportation_mode = 1

    connection = sqlite3.connect(config.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO {config.TABLE_NAME} (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, result) VALUES (?,?,?,?,?,?,?);',
        (source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode, json.dumps(expected_output)))
    connection.commit()
    cursor.close()
    connection.close()

    actual_output = db_manager.get_navigation_if_exists(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode)
    assert actual_output == expected_output

    # Cleanup added record
    cleanup_delete_record(source, destination, algorithm_id, path_percent, minimize_elevation_gain, transportation_mode)
