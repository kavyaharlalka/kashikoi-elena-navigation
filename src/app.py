from flask import Flask, render_template
# from flask_migrate import Migrate
# from models.User import db
from routes.main_blueprint import main_bp
import config

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)
app.config.from_object(__name__)
# app.config.from_object('config')
# db.init_app(app)
# migrate = Migrate(app, db)
app.register_blueprint(main_bp, url_prefix='/test')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

# if __name__ == '__main__':
#     app.debug = True
#     app.run()