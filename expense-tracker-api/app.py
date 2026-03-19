from flask import Flask, request, jsonify
from datetime import date, timedelta
from models import db, User, Expense, CATEGORIES
from auth import hash_password, check_password, generate_token, token_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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


def validate_expense(data):
    errors = []
    if not data.get('title'):
        errors.append('title is required')
    if data.get('amount') is None:
        errors.append('amount is required')
    elif not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        errors.append('amount must be a positive number')
    if not data.get('category'):
        errors.append('category is required')
    elif data['category'] not in CATEGORIES:
        errors.append(f'category must be one of: {", ".join(CATEGORIES)}')
    if not data.get('date'):
        errors.append('date is required')
    else:
        try:
            date.fromisoformat(data['date'])  # expects 'YYYY-MM-DD' format
        except ValueError:
            errors.append('date must be in YYYY-MM-DD format')
    return errors


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validate_registration(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'errors': ['email and password are required']}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password(data['password'], user.password_hash):
        return jsonify({'message': 'Invalid email or password'}), 401

    return jsonify({'token': generate_token(user.id)}), 200


@app.route('/expenses', methods=['POST'])
@token_required
def create_expense(current_user):
    data = request.get_json()
    errors = validate_expense(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    expense = Expense(
        title=data['title'],
        amount=data['amount'],
        category=data['category'],
        date=date.fromisoformat(data['date']),
        user_id=current_user.id
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense.to_dict()), 201


@app.route('/expenses', methods=['GET'])
@token_required
def get_expenses(current_user):
    query = Expense.query.filter_by(user_id=current_user.id)

    filter_param = request.args.get('filter')
    start_date   = request.args.get('start_date')
    end_date     = request.args.get('end_date')
    today        = date.today()

    if filter_param:
        offsets = {'week': 7, 'month': 30, '3months': 90}
        if filter_param not in offsets:
            return jsonify({'errors': [f'filter must be one of: {", ".join(offsets)}']}), 400
        since = today - timedelta(days=offsets[filter_param])
        query = query.filter(Expense.date >= since)

    elif start_date or end_date:
        if not start_date or not end_date:
            return jsonify({'errors': ['both start_date and end_date are required for custom range']}), 400
        try:
            start = date.fromisoformat(start_date)
            end   = date.fromisoformat(end_date)
        except ValueError:
            return jsonify({'errors': ['dates must be in YYYY-MM-DD format']}), 400
        if start > end:
            return jsonify({'errors': ['start_date must be before end_date']}), 400
        query = query.filter(Expense.date >= start, Expense.date <= end)

    page  = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # Sort by date descending and paginate the filtered query
    pagination = query.order_by(Expense.date.desc()).paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        'data':        [e.to_dict() for e in pagination.items],
        'page':        pagination.page,
        'limit':       limit,
        'total':       pagination.total,
        'total_pages': pagination.pages,
    }), 200


@app.route('/expenses/<int:expense_id>', methods=['PUT'])
@token_required
def update_expense(current_user, expense_id):
    expense = db.session.get(Expense, expense_id)
    if not expense:
        return jsonify({'message': 'Not found'}), 404

    if expense.user_id != current_user.id:
        return jsonify({'message': 'Forbidden'}), 403

    data = request.get_json()
    errors = validate_expense(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    expense.title    = data['title']
    expense.amount   = data['amount']
    expense.category = data['category']
    expense.date     = date.fromisoformat(data['date'])
    db.session.commit()
    return jsonify(expense.to_dict()), 200


@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
@token_required
def delete_expense(current_user, expense_id):
    expense = db.session.get(Expense, expense_id)
    if not expense:
        return jsonify({'message': 'Not found'}), 404

    if expense.user_id != current_user.id:
        return jsonify({'message': 'Forbidden'}), 403

    db.session.delete(expense)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)