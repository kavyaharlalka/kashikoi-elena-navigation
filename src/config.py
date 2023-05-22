import configparser
import os

os.chdir(os.path.dirname(__file__))
print(os.getcwd())

parser = configparser.SafeConfigParser()
parser.read('config.ini')

TEMPLATES_DIR = parser.get('APPLICATION', 'templates_directory')
STATIC_DIR = parser.get('APPLICATION', 'static_directory')

DATABASE_NAME = parser.get('DATABASE', 'database_name')
TABLE_NAME = parser.get('DATABASE', 'table_name')

GMAP_API_KEY = parser.get('API', 'gmap_api_key')