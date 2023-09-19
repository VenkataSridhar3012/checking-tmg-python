from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    print("hello world")
    # Your main route logic here
