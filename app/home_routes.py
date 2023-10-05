from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/api')
def index():
    response = 'Hello world ! welcome to TMG backend application'
    status_code=200
    return response, status_code
