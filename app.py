from flask import Flask, request
from multiprocessing import Value

import logging
forensics = Value('i', 0)
access = Value('i', 0)
rdata = Value('i', 0)
defaultCounter = Value('i', 0)

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)
log = logging.getLogger()

@app.route("/", defaults={"path": ""}, methods=['GET', 'POST', 'PUT'])
@app.route("/<path:path>", methods=['GET', 'POST', 'PUT'])
def echo(path):
    # Get raw data 
    data = request.get_data()
    counter = 0
    if request.path == "/forensics":
        with forensics.get_lock():
            forensics.value += 1
            counter = forensics.value
    elif request.path == "/access":
        with access.get_lock():
            access.value += 1
            counter = access.value
    elif request.path == "/rdata":
        with rdata.get_lock():
            rdata.value += 1
            counter = rdata.value        
    else
        with defaultCounter.get_lock():
            defaultCounter.value += 1
            counter = defaultCounter.value
                   
    # Make sure data isn't empty
    if not data:
        return f'Request to {request.full_path} No data provided! counter={counter}'
    # Check if data should be JSON
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Write to log
        log.info(f'Request to {request.full_path}, counter={counter}, data={request.json}')
        return request.json
    elif content_type == 'application/x-www-form-urlencoded':
        log.info(f'Request to {request.full_path}, data={request.form}')
        return request.form
    else:
        log.info(f'Request to {request.full_path}, counter={counter}, {data=}')
        return data

@app.route("/get_count")
def get_count():
    return {
        'access': access.value, 
        'forensics': security.value, 
        'rdata': rdata.value
    }
if __name__ == "__main__":
    app.run()
