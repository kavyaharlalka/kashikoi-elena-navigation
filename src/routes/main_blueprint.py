from flask import Blueprint

from controller.main_controller import home, help, about, getroute

main_bp = Blueprint('main_blueprint', __name__)
main_bp.route('/', methods=['GET'])(home)
main_bp.route('/help', methods=['GET'])(help)
main_bp.route('/about', methods=['GET'])(about)
main_bp.route('/getroute', methods=['POST'])(getroute)