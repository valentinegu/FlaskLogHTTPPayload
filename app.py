from flask import Flask, request
import logging
app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.getLogger('pika').setLevel(logging.WARNING)
log = logging.getLogger()

@app.route("/", defaults={"path": ""}, methods=['GET', 'POST', 'PUT'])
@app.route("/<path:path>", methods=['GET', 'POST', 'PUT'])
def echo(path):
    # Get raw data 
    data = request.get_data()
    # Make sure data isn't empty
    if not data:
        return f'Request to {request.full_path} No data provided!'
    # Check if data should be JSON
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Write to log
        log.info(f'Request to {request.full_path}, data={request.json}')
        return request.json
    elif content_type == 'application/x-www-form-urlencoded':
        log.info(f'Request to {request.full_path}, data={request.form}')
        return request.form
    else:
        log.info(f'Request to {request.full_path}, {data=}')
        return data

if __name__ == "__main__":
    app.run()
