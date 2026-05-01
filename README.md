# Notes API

A REST API built with FastAPI, PostgreSQL, and Docker. Supports user authentication and full CRUD operations on personal notes.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy (SQLModel)
- **Auth:** JWT (python-jose) + Password Hashing (passlib)
- **Containerization:** Docker + Docker Compose
- **Deployment:** Railway

## Features

- User registration and login
- JWT-based authentication
- Create, read, and delete personal notes
- Notes are user-scoped — users can only access their own notes
- Global error handling and structured logging
- Fully containerized with Docker

## Project Structure

```
notes_api/
├── main.py          # Routes and app entry point
├── database.py      # DB connection, session, and DB utility functions
├── models.py        # SQLModel table definitions
├── schemas.py       # Pydantic request/response schemas
├── auth.py          # JWT and password hashing logic
├── logger.py        # Logging configuration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env             # Not committed — see Environment Variables
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |

### Notes
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/notes` | Create a note | ✅ |
| GET | `/notes` | Get all notes for logged in user | ✅ |
| GET | `/notes/{id}` | Get a specific note | ✅ |
| DELETE | `/notes/{id}` | Delete a specific note | ✅ |

## Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=--pgsql_url--/notesdb
SECRET_KEYWORD=yoursecretkey
ALGORITHM=HS256
```

## Running Locally with Docker

```bash
docker compose up --build
```

API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## Running Without Docker

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Make sure PostgreSQL is running locally and `DATABASE_URL` points to `localhost`.
