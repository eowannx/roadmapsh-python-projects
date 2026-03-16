from flask import Flask, request, jsonify
from models import db, Post
from datetime import datetime, timezone

app = Flask(__name__)

# Set database name and path
# 3 slashes = relative path (instance/ folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# disables modification tracking to avoid warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Links db object to Flask app (no files yet)
db.init_app(app)

# Creates blog.db file on disk at path defined in SQLALCHEMY_DATABASE_URI
with app.app_context():
    db.create_all()


def validate_post_data(data):
    errors = []
    if not data.get('title'):
        errors.append('title is required')
    if not data.get('content'):
        errors.append('content is required')
    if not data.get('category'):
        errors.append('category is required')
    if 'tags' in data and not isinstance(data['tags'], list):
        errors.append('tags must be an array')
    return errors


# CREATE
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    errors = validate_post_data(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    post = Post(
        title=data['title'],
        content=data['content'],
        category=data['category'],
    )
    post.tags = data.get('tags', [])
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


# GET ALL + SEARCH
@app.route('/posts', methods=['GET'])
def get_posts():
    term = request.args.get('term', '').strip()
    if term:
        like = f'%{term}%' # % matches any characters
        posts = Post.query.filter( # all posts, unfiltered (e.g. [<post 1>, <post 2>, <post 3>])
            db.or_( # searches for a match in at least one
                # ilike — case-insensitive search
                Post.title.ilike(like),
                Post.content.ilike(like),
                Post.category.ilike(like),
            )
        ).all() # returns all found records as a list.
    else:
        posts = Post.query.all() # all posts, unfiltered
    return jsonify([p.to_dict() for p in posts]), 200


# GET ONE
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.to_dict()), 200


# UPDATE
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    data = request.get_json()
    errors = validate_post_data(data or {})
    if errors:
        return jsonify({'errors': errors}), 400

    post.title    = data['title']
    post.content  = data['content']
    post.category = data['category']
    post.tags     = data.get('tags', [])
    post.updated_at = datetime.now(timezone.utc)
    db.session.commit() # no db.session.add() needed - post is already tracked by session
    return jsonify(post.to_dict()), 200


# DELETE
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return '', 204 # 204 no content - the request was successful, but there is nothing to return


if __name__ == '__main__':
    app.run(debug=True)