# Expense Tracker API

A Flask-based REST API for tracking personal expenses with JWT authentication.

## Features

- User registration and login with JWT authentication
- Tokens expire after 7 days — user must re-login to get a new one
- Create, read, update and delete expenses
- Each user can only access and modify their own expenses
- Filter expenses by preset ranges (last week, month, 3 months) or a custom date range
- Paginated expense list with configurable page size
- 7 expense categories: Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others
- Data persistence with SQLite via SQLAlchemy

## Requirements

- Python 3.9+

All Python dependencies are listed in `requirements.txt` and installed in step 4 of Setup.

## Setup

1. This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd expense-tracker-api
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

> No tests are included in this project.

## API Endpoints

| Method | Endpoint | Auth required | Description |
|--------|----------|---------------|-------------|
| POST | `/register` | No | Register a new user |
| POST | `/login` | No | Login and get a token |
| POST | `/expenses` | Yes | Create an expense |
| GET | `/expenses` | Yes | Get all your expenses (paginated) |
| PUT | `/expenses/<id>` | Yes | Update an expense |
| DELETE | `/expenses/<id>` | Yes | Delete an expense |

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

Example error `400 Bad Request` (missing fields or duplicate email):
```json
{
  "errors": ["email is required"]
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

Example error `401 Unauthorized` (wrong email or password):
```json
{
  "message": "Invalid email or password"
}
```

### Create an Expense
```
POST /expenses
```
```json
{
  "title": "Weekly groceries",
  "amount": 45.50,
  "category": "Groceries",
  "date": "2026-03-19"
}
```

The `category` field must be exactly one of: `Groceries`, `Leisure`, `Electronics`, `Utilities`, `Clothing`, `Health`, `Others`.

Example response `201 Created`:
```json
{
  "id": 1,
  "title": "Weekly groceries",
  "amount": 45.50,
  "category": "Groceries",
  "date": "2026-03-19"
}
```

Example error `400 Bad Request` (missing or invalid fields):
```json
{
  "errors": ["amount must be a positive number", "category must be one of: Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others"]
}
```

### Get Expenses

**Pagination** via query params: `?page=1&limit=10` (defaults: page=1, limit=10)

**Preset date filter** via `?filter=<value>` — filters expenses from the last N days up to today:

| Value | Range |
|-------|-------|
| `week` | Last 7 days |
| `month` | Last 30 days |
| `3months` | Last 90 days |

**Custom date range** via `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` — both params are required together.

`filter` and `start_date`/`end_date` are mutually exclusive — if `filter` is provided, the date range params are ignored.

```
GET /expenses
GET /expenses?filter=month
GET /expenses?start_date=2026-01-01&end_date=2026-03-01
GET /expenses?page=2&limit=5
```

Example response `200 OK`:
```json
{
  "data": [
    {
      "id": 1,
      "title": "Weekly groceries",
      "amount": 45.50,
      "category": "Groceries",
      "date": "2026-03-19"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 1,
  "total_pages": 1
}
```

Example error `400 Bad Request` (invalid filter value):
```json
{
  "errors": ["filter must be one of: week, month, 3months"]
}
```

### Update an Expense

All fields are required — PUT fully replaces the object. Missing or invalid fields return `400 Bad Request` with an `errors` array.

```
PUT /expenses/<id>
```
```json
{
  "title": "Weekly groceries",
  "amount": 52.00,
  "category": "Groceries",
  "date": "2026-03-19"
}
```

Example response `200 OK`:
```json
{
  "id": 1,
  "title": "Weekly groceries",
  "amount": 52.00,
  "category": "Groceries",
  "date": "2026-03-19"
}
```

Example error `403 Forbidden` (trying to update another user's expense):
```json
{
  "message": "Forbidden"
}
```

### Delete an Expense
```
DELETE /expenses/<id>
```

Example response `204 No Content`

Example error `404 Not Found`:
```json
{
  "message": "Not found"
}
```

## Error Reference

| Status | When it occurs |
|--------|----------------|
| `400` | Missing or invalid request fields |
| `401` | Missing, expired, or invalid token; wrong login credentials |
| `403` | Trying to modify another user's expense |
| `404` | Expense ID does not exist |

## Project Structure

### File Structure

```
expense-tracker-api/
├── app.py           # Flask app, routes and request handling
├── auth.py          # Password hashing, JWT generation and token_required decorator
├── models.py        # User and Expense models
├── requirements.txt
├── .env             # Secret key (not committed to git)
├── .gitignore
├── README.md
└── instance/
    └── expenses.db  # SQLite database (auto-generated)
```

### Database Structure

Both models are stored in a single `expenses.db` file in separate tables:

```
expenses.db
├── users
│   ├── id
│   ├── name
│   ├── email          (unique)
│   ├── password_hash
│   └── created_at
│
└── expenses
    ├── id
    ├── title
    ├── amount
    ├── category
    ├── date
    ├── user_id        (foreign key → users.id)
    └── created_at
```

## Project Source

This project is based on the [Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api) challenge from [roadmap.sh](https://roadmap.sh).