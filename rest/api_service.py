from flask import Flask
from flask import request
from flask import jsonify
import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))
app = Flask(__name__)

from parser.parser import JsonParser
from rest.exceptions import UnauthorizedRequestError


@app.route('/')
def root():
    message = {
        "hi": "this is not the endpoint you're looking for, "
              "maybe try /parse, don't forget to auth (re_is_awesome)"
    }
    return jsonify(message), 200


@app.route('/parse', methods=['POST'])
def message_me():
    headers = request.headers
    magicauth = headers.get("magicauth", None)
    if not magicauth:
        raise UnauthorizedRequestError('no auth header supplied')
    elif magicauth != 're_is_awesome':
        raise UnauthorizedRequestError('incorrect auth')

    query_string = request.query_string.decode("utf-8")
    nest_keys = query_string.replace("nest=", "").split("&")

    content = request.get_json(force=True)
    convert = JsonParser()
    parsed = convert.parse(content, nest_keys)

    return jsonify(parsed)


@app.errorhandler(UnauthorizedRequestError)
def dont_let_me_pass(error):
    yer_error = {
        'error': str(error),
    }
    return jsonify(yer_error), 401


@app.errorhandler(404)
def not_found(error):
    yer_error = {
        'error': 'not found',
        'status': 404
    }
    return jsonify(yer_error), 404


@app.errorhandler(Exception)
def error_all_the_things(error):
    yer_error = {
        'exception': str(error),
        'status': 500
    }
    return jsonify(yer_error), 500


if __name__ == '__main__':
    app.run("0.0.0.0")
