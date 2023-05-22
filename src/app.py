from flask import Flask
from routes.main_blueprint import main_bp
import config
import os

os.chdir(os.path.dirname(__file__))
print(os.getcwd())

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.config.from_object(__name__)
app.register_blueprint(main_bp, url_prefix='/')
