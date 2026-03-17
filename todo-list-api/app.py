from flask import Flask, request, jsonify
from models import db, User, Todo
from auth import hash_password, check_password, generate_token, token_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' # set database name and path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disables modification tracking to avoid warnings

db.init_app(app) # links db object to Flask app (no files yet)

# Creates blog.db file on disk at path defined in SQLALCHEMY_DATABASE_URI
with app.app_context():
    db.create_all()


def validate_registration(data):
    errors = []
    if not data.get('name'):
        errors.append('name is required')
    if not data.get('email'):
        errors.append('email is required')
    if not data.get('password'):
        errors.append('password is required')
    return errors


def validate_todo(data):
    errors = []
    if not data.get('title'):
        errors.append('title is required')
    if not data.get('description'):
        errors.append('description is required')
    return errors


# REGISTER
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validate_registration(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    # without .first(), .all() or .limit() the query object is just a description of the query — no data is fetched from DB
    # .first() fetches only the first matching user and stops — unlike .all() which loads all results into memory
    # or .limit(n) which loads first n results — here we only need to know if email exists, so .first() is enough
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'errors': ['email already exists']}), 400

    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hash_password(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'token': generate_token(user.id)}), 201


# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'errors': ['email and password are required']}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password(data['password'], user.password_hash):
        return jsonify({'message': 'Invalid email or password'}), 401

    return jsonify({'token': generate_token(user.id)}), 200


# CREATE TODO
@app.route('/todos', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()
    errors = validate_todo(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    todo = Todo(
        title=data['title'],
        description=data['description'],
        user_id=current_user.id
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


# GET TODOS
@app.route('/todos', methods=['GET'])
@token_required
def get_todos(current_user):
    page  = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # fetch todos belonging to current user only, split into pages to avoid loading all records at once
    # error_out=False — return empty list instead of 404 if page doesn't exist
    pagination = Todo.query.filter_by(user_id=current_user.id)\
        .paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        'data':  [t.to_dict() for t in pagination.items],
        'page':  pagination.page,
        'limit': limit,
        'total': pagination.total,
        'total_pages': pagination.pages,
    }), 200


# UPDATE TODO
@app.route('/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'message': 'Not found'}), 404

    # todo ids are global across the table — any user can request /todos/1
    # this check ensures the todo belongs to current user and not another user
    if todo.user_id != current_user.id:
        return jsonify({'message': 'Forbidden'}), 403

    # PUT fully replaces the object — both fields must be provided
    # if description is missing, it would be overwritten with None in DB
    data = request.get_json()
    errors = validate_todo(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    todo.title       = data['title']
    todo.description = data['description']
    db.session.commit()
    return jsonify(todo.to_dict()), 200


# DELETE TODO
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'message': 'Not found'}), 404

    if todo.user_id != current_user.id:
        return jsonify({'message': 'Forbidden'}), 403

    db.session.delete(todo)
    db.session.commit
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)