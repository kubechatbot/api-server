from flask import Blueprint
user_route = Blueprint('user_page', __name__, url_prefix="/user")

from .dashboard import *