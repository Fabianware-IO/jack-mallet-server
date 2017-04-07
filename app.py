"""Main Application Endpoint"""

from flask import make_response, request, Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson import json_util
import json
import uuid
import datetime

app = Flask(__name__)
CORS(app)

connect_string = 'mongodb://jm-readwrite:jackmallet123!@ds149700.mlab.com:49700/jack-mallet'
app.config['MONGO_DBNAME'] = 'jack-mallet'
app.config['MONGO_URI'] = connect_string

mongo = PyMongo(app)

# API Base Path
API_PATH = '/api/v1'
# Routes
ROUTE_VERSION = API_PATH + '/version.properties'
ROUTE_DATA = API_PATH + '/data'
ROUTE_LOGIN = API_PATH + '/login'
ROUTE_SUBSCRIBERS = API_PATH + '/subscribers'

def to_json(data):
    return json.dumps(data, default=json_util.default)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"

@app.route(ROUTE_VERSION, methods=['GET'])
def version():
    return jsonify({'version': 'v 0.1.42'})

@app.route(ROUTE_LOGIN, methods=['POST'])
def login():
    content = request.get_json()
    user = mongo.db.users.find_one({'username': content['username']})
    if (user) and (user['password'] == content['password']):
        token = str(uuid.uuid4())
        token_age = datetime.datetime.utcnow() + datetime.timedelta(minutes=525600)
        update = mongo.db.users.update_one(
            {'username': user['username']},
            {'$set':{"authentication_token": token, "token_age": token_age}})
        return jsonify(
            {'response':{
                'user':{'username': user['username'], 'fullName': user['fullName'],
                        'authentication_token': token, "token_age": token_age}}})
    else:
        return make_response(jsonify({'error': 'unauthorized'}), 401)

@app.route(ROUTE_DATA, methods=['GET'])
def data():
    data = mongo.db.data
    rows = []
    results = data.find()
    for result in results:
        rows.append(result)
    return to_json(rows)

@app.route(ROUTE_SUBSCRIBERS, methods=['GET'])
def subscribers():
    results = mongo.db.subscribers.find()
    rows = []
    for result in results:
        rows.append(result)
    return to_json(rows)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
