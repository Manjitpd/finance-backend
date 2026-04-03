# 📊 Finance Dashboard Backend (FastAPI)

## 🚀 Overview

This project is a backend system for a **Finance Dashboard** that manages financial records, user roles, and analytics.

It demonstrates:

* Clean backend architecture
* Role-Based Access Control (RBAC)
* Financial data processing
* Dashboard analytics APIs
* PostgreSQL + Alembic migrations

---

## 🌐 Live API

API Documentation (Swagger UI):  
https://finance-backend-fz9d.onrender.com/docs

Frontend App:
https://finance-dashboard-frontend-amber.vercel.app



---
## 🔐 Demo Credentials

Email: ritik@gmail.com  
Password: ritik@123  

### How to Use

1. Open Swagger UI  
2. Call POST /auth/login  
3. Copy access_token  
4. Click "Authorize" 🔒  
5. Paste:
   Bearer <your_token>  
6. Now you can use all APIs

---

## 🏗️ Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy (Async)
* **Migrations:** Alembic
* **Authentication:** JWT
* **Environment Config:** Pydantic Settings

---

## 📁 Project Structure

```
app/
 ├── main.py
 ├── core/
 ├── models/
 ├── schemas/
 ├── api/
 ├── services/
 ├── db/
```

### Architecture Approach

* **Routes** → Handle HTTP requests
* **Services** → Business logic & DB operations
* **Models** → Database schema
* **Schemas** → Request/Response validation

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <repo-url>
cd finance-backend
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate 
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/finance_db
SYNC_DATABASE_URL=postgresql://postgres:password@localhost:5432/finance_db

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=120
```

---

### 5. Run Migrations

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

---

### 6. Start Server

```bash
uvicorn app.main:app --reload
```

---

## 🔐 Authentication

* JWT-based authentication
* Token required for protected routes

### Login API

```
POST /auth/login
```

---

## 👥 Roles & Permissions

| Role    | Permissions                          |
| ------- | ------------------------------------ |
| Viewer  | Only dashboard access                |
| Analyst | View financial records + dashboard   |
| Admin   | Full access                          |

---

## 📌 API Endpoints

### 🔑 Auth

* `POST /auth/login` → Login & get token

---

### 👤 Users (Admin Only)

* `POST /users/` → Create user
* `GET /users/` → Get all users (includes active & inactive)
* `GET /users/{id}` → Get user by ID
* `PUT /users/{id}` → Update user (Password is optional keeps old password if not provided)
* `DELETE /users/{id}` → Soft delete




---

### 💰 Finance Records

#### Create Record (Admin)

```
POST /records/
```

#### Get Records (Admin, Analyst)

Supports:

* Filtering (type, category, date range)
* Pagination

```
GET /records/?type=income&category=food&start_date=2026-01-01&end_date=2026-12-31&page=1&limit=10
```

#### Update Record (Admin)

```
PUT /records/{id}
```

#### Delete Record (Soft Delete) (Admin)

```
DELETE /records/{id}
```

---

### 📊 Dashboard

#### Summary API (All Roles)

```
GET /dashboard/summary
```

Returns:

* Total income
* Total expenses
* Net balance
* Category-wise totals
* Recent transactions
* Monthly trends

---

## 🔍 Features Implemented

✅ JWT Authentication
✅ Role-Based Access Control
✅ CRUD for financial records
✅ Filtering (type, category, date range)
✅ Pagination
✅ Soft delete
✅ Dashboard analytics
✅ Clean architecture (services layer)
✅ PostgreSQL with Alembic

---

## ⚠️ Assumptions Made

* Passwords are stored as plain text (for simplicity)
* Role is stored directly in user table
* No refresh token implementation
* Single-tenant system (no organization separation)

---

## ⚖️ Tradeoffs

* Used **simple RBAC** instead of permission-based system (to keep scope focused)
* Did not implement password hashing to reduce complexity
* Used basic error handling instead of global exception middleware

---

## 🚀 Possible Improvements

* Add password hashing (bcrypt)
* Add refresh tokens
* Implement permission-based RBAC
* Add unit & integration tests
* Add API documentation (Swagger enhancements)
* Add Docker support

---

## 🧠 Key Design Decisions

* **Service Layer Pattern** → Keeps business logic separate
* **Async SQLAlchemy** → Better performance
* **Soft Delete** → Data recovery support
* **Single Summary API** → Efficient dashboard data fetch

---

## 📌 Conclusion

This project demonstrates backend fundamentals including:

* API design
* Data modeling
* Access control
* Scalable structure

The focus was on **clarity, maintainability, and correct backend practices** rather than unnecessary complexity.

---
