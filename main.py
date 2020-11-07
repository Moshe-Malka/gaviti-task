import json,  os
from bson import json_util
from uuid import uuid4
from celery import Celery
from flask import Flask, abort, request, jsonify, send_from_directory
from flask_pymongo import PyMongo

flask_app = Flask(__name__)

# Make Celery App
def make_celery(app):
    redis_url = 'redis://localhost:6379'
    celery = Celery(
        app.import_name,
        backend=redis_url,
        broker=redis_url
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)

flask_app.config["OUTPUT_FILES_FOLDER"] = f"{os.getcwd()}/output"
# PyMongo 
flask_app.config['MONGO_URI'] = 'mongodb://localhost:27017/gaviti'
mongo = PyMongo(flask_app)

@celery.task()
def write_file(fname, data):
    with open(fname, 'w') as f:
        json.dump(data, f)

@flask_app.route('/search', methods=['POST'])
def search():
    try:
        # Getting request data and prepering a save path for the response data.
        data = request.get_json()
        if 'startDate' not in data or 'endDate' not in data: raise Exception('Invalid message')
        fname = str(uuid4())
        full_path = f"{flask_app.config['OUTPUT_FILES_FOLDER']}/{fname}.json"
        # getting results  from mongodb
        results = mongo.db.mock_data.find({
            'timestamp': {
                '$gte': data.get('startDate'),
                '$lt': data.get('endDate')
                }
            }
        )
        results_raw = json.loads(json_util.dumps(list(results)))    # this is for handeling mongodb json.
        if results_raw:
            write_file(full_path, results_raw)
            return jsonify(statusCode=200, results_link=f"http://127.0.0.1:5000/download/{fname}"), 200
        else:
            return jsonify(statusCode=404, error="No Results"), 404
    except Exception as e:
        print(e)
        return jsonify(statusCode=500, error="Internal Server Error"), 500

@flask_app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(flask_app.config["OUTPUT_FILES_FOLDER"], filename=f"{filename}.json", as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify(statusCode=500, error=str(e)), 500

if __name__ == '__main__':
    print("Starting...")
    flask_app.run(threaded=True, port=5000)
    
