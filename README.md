# 🎬 CineVault

CineVault is a full-stack, Dockerized movie management platform built to store, organize, and manage film data in a structured and scalable way.

It provides a secure REST API for managing movies, actors, directors, genres, and languages — along with authentication, pagination, and search functionality. This project demonstrates backend engineering practices including containerization, relational database design, authentication systems, and production-style API development.

---

## 🚀 Features

- 🔐 JWT-based Authentication (Register / Login)
- 🎞️ Movie CRUD Operations
- 👥 Actor & Director Relationships
- 🏷️ Genre & Language Tagging
- 🔎 Movie Search by Title
- 📄 Pagination Support
- 🗄️ MySQL Relational Database
- 🐳 Dockerized Deployment (Flask + MySQL)
- 🌐 RESTful API Architecture

---

## 🧱 Tech Stack

| Layer | Technology |
|------|-------------|
| Backend | Flask (Python) |
| ORM | SQLAlchemy |
| Authentication | JWT (Flask-JWT-Extended) |
| Database | MySQL |
| Containerization | Docker & Docker Compose |
| WSGI Server | Gunicorn |
| Configuration | Environment Variables (.env) |

---

## 📁 Project Layout

```
CineVault/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
├── bd/
│   └── webserver.sql
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── run.sh
├── run.ps1
└── README.md
```

---

## ⚙️ Configuration

The application uses environment variables for secrets and database credentials.

### Create `.env` file

**Windows (PowerShell)**

```
copy .env.example .env
```

**Linux / macOS**

```
cp .env.example .env
```

---

### Example `.env` values

```
MYSQL_ROOT_PASSWORD=YourRootPassHere
MYSQL_DATABASE=CineVault
MYSQL_USER=cineuser
MYSQL_PASSWORD=YourDBPassHere

DB_HOST=db
DB_USER=cineuser
DB_PASS=YourDBPassHere
DB_NAME=CineVault

JWT_SECRET=generate_a_long_random_secret_here
PORT=5000
```

⚠️ Never commit `.env` to GitHub.

---

## 🐳 Run with Docker (Recommended)

### Start containers

```
docker-compose up --build
```

### Services started

- MySQL database
- Flask API served via Gunicorn

App URL:

```
http://localhost:8000
```

---

### Stop containers

```
docker-compose down
```

---

## 💻 Run Locally (Without Docker)

### 1️⃣ Create virtual environment

```
python -m venv venv
```

Activate:

```
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### 2️⃣ Install dependencies

```
pip install -r app/requirements.txt
```

---

### 3️⃣ Configure database

- Start MySQL locally or remotely
- Ensure credentials match `.env`
- Optionally run:

```
bd/webserver.sql
```

---

### 4️⃣ Run Flask app

```
python app/app.py
```

App runs at:

```
http://localhost:5000
```

---

## 🔐 Authentication Flow (JWT)

### Register

**POST** `/auth/register`

```
{
  "username": "admin",
  "password": "your_password"
}
```

---

### Login

**POST** `/auth/login`

```
{
  "username": "admin",
  "password": "your_password"
}
```

Response:

```
{ "access_token": "eyJ..." }
```

Use token:

```
Authorization: Bearer <access_token>
```

---

## 📄 API Summary

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | /auth/register | Create user |
| POST | /auth/login | Login & get JWT |
| GET | /api/movies | List movies |
| GET | /api/movies/:id | Get movie details |
| POST | /api/movies | Create movie (Protected) |
| DELETE | /api/movies/:id | Delete movie (Protected) |
| POST | /admin/seed | Seed sample data |

---

## 🔎 Pagination & Search

Example:

```
GET /api/movies?page=1&per_page=10&q=inception
```

Query Parameters:

- `page` → Page number  
- `per_page` → Results per page  
- `q` → Search by movie title  

---

## 🛡️ Security Notes

- Secrets stored in `.env`
- JWT tokens signed securely
- Passwords hashed before storage
- Database isolated via Docker network

---

## 📌 Future Enhancements

- Integrate rating and discussion forums
- Poster uploads
- Better UI/UX for frontend
- Frontend dashboard
- Cloud deployment

---

## 📜 License

MIT License — Free to use and modify.
