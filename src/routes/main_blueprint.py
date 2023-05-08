from flask import Blueprint

from controller.main_controller import home, help, findRoute

main_bp = Blueprint('main_blueprint', __name__)
main_bp.route('/', methods=['GET'])(help)
main_bp.route('/help', methods=['GET'])(home)
main_bp.route('/findroute', methods=['POST'])(findRoute)