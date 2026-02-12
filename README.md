# CineVault — Dockerized Flask App

## Quick Start

### 1️⃣ Setup environment

Copy the example env file:

Linux/macOS:
```
cp .env.example .env
```

Windows PowerShell:
```
copy .env.example .env
```

Edit `.env` and set secure passwords + JWT secret.

---

### 2️⃣ Run the app

Linux/macOS:
```
./run.sh
```

Windows:
```
./run.ps1
```

Or manually:
```
docker-compose up --build
```

---

## App URL
http://localhost:8000

---

## Auth Flow

Register:
```
POST /auth/register
{
  "username": "admin",
  "password": "StrongPass123"
}
```

Login → returns JWT token:
```
POST /auth/login
```

Use token:
```
Authorization: Bearer <token>
```

---

## Pagination & Search

```
GET /api/movies?page=1&per_page=10&q=batman
```

---

## Publish to GitHub

```
git init
git add .
git commit -m "CineVault Dockerized"
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

---

## Notes

- Change all passwords in `.env`
- Do NOT commit `.env`
- Use Nginx + HTTPS for production