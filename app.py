from index_page import *
from user_page import *
from flask import Flask
app = Flask(__name__)
app.register_blueprint(index_route)
app.register_blueprint(user_route)

if __name__ == '__main__':
    app.run()