# Blogging Platform API

A Flask-based REST API for a personal blogging platform with full CRUD operations and search functionality.

## Features

- Create, read, update and delete blog posts
- Filter posts by search term across title, content and category fields
- Data persistence with SQLite via SQLAlchemy

## Requirements

- Python 3.9+

All Python dependencies are listed in `requirements.txt` and installed in step 3 of Setup.

## Setup

1. This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd blogging-platform-api
```

2. Create and activate virtual environment
```
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the application
```
python app.py
```

## API Endpoints

| Method | Endpoint | Description | Body required |
|--------|----------|-------------|---------------|
| POST | `/posts` | Create a post | Yes |
| GET | `/posts` | Get all posts | No |
| GET | `/posts?term=<term>` | Search posts | No |
| GET | `/posts/<id>` | Get a single post | No |
| PUT | `/posts/<id>` | Update a post | Yes |
| DELETE | `/posts/<id>` | Delete a post | No |

### Create a post
```
POST /posts
```
```json
{
  "title": "My First Post",
  "content": "Hello world",
  "category": "Tech",
  "tags": ["Python", "Flask"]
}
```

Example response `201 Created`:
```json
{
  "id": 1,
  "title": "My First Post",
  "content": "Hello world",
  "category": "Tech",
  "tags": ["Python", "Flask"],
  "createdAt": "2026-03-16T07:21:35Z",
  "updatedAt": "2026-03-16T07:21:35Z"
}
```

### Get all posts
```
GET /posts
```

Example response `200 OK`:
```json
[
  {
    "id": 1,
    "title": "My First Post",
    "content": "Hello world",
    "category": "Tech",
    "tags": ["Python", "Flask"],
    "createdAt": "2026-03-16T07:21:35Z",
    "updatedAt": "2026-03-16T07:21:35Z"
  },
  {
    "id": 2,
    "title": "My Second Post",
    "content": "Hello again",
    "category": "News",
    "tags": [],
    "createdAt": "2026-03-16T08:00:00Z",
    "updatedAt": "2026-03-16T08:00:00Z"
  }
]
```

### Search posts
```
GET /posts?term=tech
```
Searches across `title`, `content` and `category` fields (case-insensitive).

Example response `200 OK`:
```json
[
  {
    "id": 1,
    "title": "My First Post",
    "content": "Hello world",
    "category": "Tech",
    "tags": ["Python", "Flask"],
    "createdAt": "2026-03-16T07:21:35Z",
    "updatedAt": "2026-03-16T07:21:35Z"
  }
]
```

### Get a single post
```
GET /posts/<id>
```

Example response `200 OK`:
```json
{
  "id": 1,
  "title": "My First Post",
  "content": "Hello world",
  "category": "Tech",
  "tags": ["Python", "Flask"],
  "createdAt": "2026-03-16T07:21:35Z",
  "updatedAt": "2026-03-16T07:21:35Z"
}
```

### Update a post
```
PUT /posts/<id>
```
```json
{
  "title": "Updated Post",
  "content": "Updated content",
  "category": "Tech",
  "tags": ["Python"]
}
```

Example response `200 OK`:
```json
{
  "id": 1,
  "title": "Updated Post",
  "content": "Updated content",
  "category": "Tech",
  "tags": ["Python"],
  "createdAt": "2026-03-16T07:21:35Z",
  "updatedAt": "2026-03-16T07:22:28Z"
}
```

### Delete a post
```
DELETE /posts/<id>
```

Example response `204 No Content`

## Project Structure

```
blogging-platform-api/
├── app.py          # Flask app, routes and request handling
├── models.py       # Post model and database setup
├── requirements.txt
└── instance/
    └── blog.db     # SQLite database (auto-generated)
```


## Project Source

This project is based on the [Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api) challenge from [roadmap.sh](https://roadmap.sh).