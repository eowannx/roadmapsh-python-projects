# Todo List API

A Flask-based REST API for managing personal todos with JWT authentication.

## Features

- User registration and login with JWT authentication
- Tokens expire after 7 days — user must re-login to get a new one
- Create, read, update and delete todos
- Each user can only access and modify their own todos
- Paginated todo list with configurable page size
- Data persistence with SQLite via SQLAlchemy

## Requirements

- Python 3.9+

All Python dependencies are listed in `requirements.txt` and installed in step 4 of Setup.

## Setup

1. This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd todo-list-api
```

2. Create and activate virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Create a `.env` file in the project root and add your own secret key:

```
SECRET_KEY=your_secret_key_here
```

The secret key is used to sign JWT tokens — use any long random string.

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python app.py
```

## API Endpoints

| Method | Endpoint | Auth required | Description |
|--------|----------|---------------|-------------|
| POST | `/register` | No | Register a new user |
| POST | `/login` | No | Login and get a token |
| POST | `/todos` | Yes | Create a todo |
| GET | `/todos` | Yes | Get all your todos (paginated) |
| PUT | `/todos/<id>` | Yes | Update a todo |
| DELETE | `/todos/<id>` | Yes | Delete a todo |

Authenticated routes require a JWT token in the `Authorization` header:

```
Authorization: <your_token>
```

### Register
```
POST /register
```
```json
{
  "name": "John",
  "email": "john@example.com",
  "password": "secret123"
}
```

Example response `201 Created`:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login
```
POST /login
```
```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

Example response `200 OK`:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create a Todo
```
POST /todos
```
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

Example response `201 Created`:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

### Get Todos

Supports pagination via query params: `/todos?page=1&limit=10` (defaults: page=1, limit=10)

```
GET /todos
```

Example response `200 OK`:
```json
{
  "data": [
    { "id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread" }
  ],
  "page": 1,
  "limit": 10,
  "total": 1,
  "total_pages": 1
}
```

### Update a Todo

Both `title` and `description` are required — PUT fully replaces the object.

```
PUT /todos/<id>
```
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter"
}
```

Example response `200 OK`:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, butter"
}
```

### Delete a Todo
```
DELETE /todos/<id>
```

Example response `204 No Content`

## Project Structure

### File Structure

```
todo-list-api/
├── app.py           # Flask app, routes and request handling
├── auth.py          # Password hashing, JWT generation and token_required decorator
├── models.py        # User and Todo models
├── requirements.txt
├── .env             # Secret key (not committed to git)
├── .gitignore
├── README.md
└── instance/
    └── todo.db      # SQLite database (auto-generated)
```

### Database Structure

Both models are stored in a single `todo.db` file in separate tables:

```
todo.db
├── users
│   ├── id
│   ├── name
│   ├── email          (unique)
│   ├── password_hash
│   └── created_at
│
└── todos
    ├── id
    ├── title
    ├── description
    ├── user_id        (foreign key → users.id)
    └── created_at
```

## Project Source

This project is based on the [Todo List API](https://roadmap.sh/projects/todo-list-api) challenge from [roadmap.sh](https://roadmap.sh).