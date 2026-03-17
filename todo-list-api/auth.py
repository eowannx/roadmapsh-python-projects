import os
import jwt
import bcrypt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
from models import User

# Load environment variables from .env file into the program
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Converts a password (string) to bcrypt hash with a random 22-character salt embedded inside
# This salt ensures identical passwords produce different hashes for security
def hash_password(password):
    # bcrypt.hashpw(password, salt)
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Extracts the embedded salt from the hash and re-hashes password to compare
# Compares the result with the stored hash to verify the password is correct
def check_password(password, hashed):
    # bcrypt.checkpw(password, hashed_password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Generates a JWT (JSON Web Token) for stateless authentication without storing sessions
# Token structure: HEADER.PAYLOAD.SIGNATURE
# - HEADER: algorithm type (HS256)
# - PAYLOAD: user_id and exp (expiration in 7 days)
# - SIGNATURE: cryptographic hash of header+payload signed with SECRET_KEY
# Each token is unique because exp is generated with current datetime, so signature differs each time
# Client stores token locally and sends it with every authorized request for authentication
# After 7 days, token expires and user must re-login to generate a new one
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Verifies JWT token by recalculating signature from header+payload using SECRET_KEY
# If signatures match and token hasn't expired, extracts user_id from payload via jwt.decode()
# Uses extracted user_id to identify current user and authorize the request
# If token is expired or signature doesn't match, raises InvalidTokenError

# Decorator — not just a function that runs before another function,
# but a function that WRAPS another function: token_required(get_todos)
# meaning get_todos is passed directly into token_required and used inside it
# This lets us add extra logic (token check) while keeping the original function unchanged — for flexibility
def token_required(f):
    @wraps(f) # preserves metadata of the original wrapped function (f)
              # so each route using this decorator keeps its own __name__, and not 'decorated'
    def decorated(*args, **kwargs): # *args, **kwargs are required because the original function accepts arguments
                                    # without them, decorated wouldn't know what to pass into f() when calling it
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Unauthorized'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256']) # decrypt and verify token signature
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Unauthorized'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(current_user, *args, **kwargs) # return passes the result back up to Flask so it can send response to client
    return decorated # returning decorated (not calling it) means f won't execute immediately —
                     # it will only run when an actual HTTP request comes in, just like a normal function call