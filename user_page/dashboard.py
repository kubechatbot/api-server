from flask import render_template
from . import user_route

@user_route.route('/<id>', methods=['GET'])
def user_dashboard(id=None):
    return "this page is {id}"