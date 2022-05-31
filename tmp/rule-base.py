from flask import Flask, request

app = Flask(__name__)
db = {}

@app.route('/')
def hello():
    return 'Hello Kubechat!'
    
@app.route('/create', methods=['POST'])
def create():
    params = request.get_json()
    user_id = params['user_id']
    print(params)
    if db.get(user_id):
        return "Please insert user id"

    else:
        db[user_id] = {}
    for key in params.keys():
            if key != 'user_id':
                db[user_id][key] = params[key]
    
    return "Rule is created"
            

@app.route('/search/<user_id>/<word>')
def search(user_id, word):
    print(db)
    return db[user_id][word]
    
@app.route('/delete', methods=['POST'])
def delete():
    params = request.get_json()
    user_id = params['user_id']

    for key in params.keys():
        if key in db[user_id]:
            del db[user_id][key]
    return "All rules are deleted"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)