import jwt
from flask import Flask, jsonify, request, make_response
from datetime import datetime, timedelta
from functools import wraps
app = Flask(__name__)

app.config['SECRET_KEY'] = 'onesecret_key'

USER_LIST = {'user1': 'password', 'user2': 'password'}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'Token is missing'}), 403        
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'], algorithms='HS256')
            
        except Exception as e:
            print("Exception: ", e)
            return jsonify({"message" : "Token is invalid"}), 403
        
        return f(*args, **kwargs)
    return decorated
    

@app.route('/unprotected')
def unprotected():
    return jsonify({"message": "Anyone can view this"})


@app.route('/protected')
@token_required
def protected():
    return jsonify({"message":"This is only available for people with valid tokens"})

@app.route('/login')
def login():
    auth = request.authorization
    
    if auth and auth.username in USER_LIST and auth.password == USER_LIST[auth.username]:
        
        token = jwt.encode(
            {
            'user':auth.username,
            'exp':datetime.utcnow() + timedelta(minutes=30)
            },
            app.config['SECRET_KEY']
            )
        print(token)
        return jsonify({'token': token})
        
    
    return make_response('Could not verity!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
