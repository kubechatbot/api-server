from flask import render_template
from . import index_route

@index_route.route('/')
def index():
    return 'index'

@index_route.route('/login', methods=['GET'])
def login_get():
    return 'login'