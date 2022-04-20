from flask import Blueprint
index_route = Blueprint('index_page', __name__, url_prefix="/")

from .index import *
from .login import *