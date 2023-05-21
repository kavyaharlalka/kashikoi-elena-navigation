from flask import Flask
from routes.main_blueprint import main_bp
import config

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.config.from_object(__name__)
# app.config.from_object('config')
# db.init_app(app)
# migrate = Migrate(app, db)
app.register_blueprint(main_bp, url_prefix='/')
