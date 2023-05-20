from flask import Blueprint

from controller.main_controller import home, help, getroute

main_bp = Blueprint('main_blueprint', __name__)
main_bp.route('/', methods=['GET'])(home)
main_bp.route('/getroute', methods=['POST'])(getroute)