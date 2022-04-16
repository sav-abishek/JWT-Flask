from encodings import utf_8
from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sav'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'msg': 'Missing Token!!'}, 403)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'msg': 'Invalid Token!!'}, 403)

        return f(*args, **kwargs)
    return decorated


@app.route('/protected')
@token_required
def proc():
    return jsonify({'msg': 'Protected Content'})


@app.route('/unprotected')
def unproc():
    return jsonify({'msg': 'Un-Protected Content'})


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'verify': 'sav', 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})
    return make_response('Cound not verify', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
