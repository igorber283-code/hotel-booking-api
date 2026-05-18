# 🏨 Hotel Booking API

![Docker](https://img.shields.io/badge/Docker-containerized-blue?style=flat-square&logo=docker)
![Pytest](https://img.shields.io/badge/Tests-10%20passed%20%2F%20100%25-success?style=flat-square&logo=pytest)
![Deployment](https://img.shields.io/badge/Deployment-VPS%20%7C%20Live-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen?style=flat-square)


🔗 Live Demo (Swagger UI): http://92.246.137.125:8000/docs#/

A robust, high-performance backend booking system built with **FastAPI**, **PostgreSQL**, and **Async SQLAlchemy**. This project demonstrates production-grade expertise in asynchronous Python programming, database transaction management, enterprise-level containerization, and pessimistic concurrency control.

---

## 🚀 Tech Stack

- **Framework:** FastAPI (Asynchronous)
- **Database:** PostgreSQL (explicit connection pooling)
- **Caching & In-Memory Storage:** Redis
- **ORM:** SQLAlchemy 2.0 (Async Engine & Declarative Mapping)
- **Migrations:** Alembic
- **Authentication:** JWT (AuthX / custom JOSE implementation)
- **Validation:** Pydantic v2
- **Testing:** Pytest (integration, async & concurrency/cancellation stress tests)
- **Containerization:** Docker & Docker Compose (multi-container setup)

---

## 📌 Key Features & Engineering Highlights

### 🔐 Authentication & Security

- Secure user registration and JWT-based stateless authentication
- Role-Based Access Control (RBAC)
- Password hashing with **bcrypt**
- Automated access/refresh token lifecycle management

### 🏨 Hotel & Room Management

- Dynamic hotel listings with advanced filtering and search
- Real-time room availability calculation
- High-performance caching layer using **Redis** for search queries to reduce DB load
- Structured room classification
- Automated seasonal pricing logic

### 📅 Advanced Booking Engine & Concurrency Control

- **Atomic transactions** using pessimistic locking (`SELECT ... FOR UPDATE`)
- Strict validation of booking date ranges (`date_from < date_to`)
- Guaranteed prevention of overlapping and double bookings
- Designed to safely handle high-load concurrent booking attempts

---

## 🧠 Software Architecture

The project follows a scalable **Layered Modular Architecture**, aligned with enterprise backend standards.

```
app/
├── api/          # FastAPI routers, endpoints, dependencies
├── services/     # Business logic layer (rules, pricing, validations, caching)
├── dao/          # Data Access Objects (isolated DB operations)
├── models/       # SQLAlchemy declarative models
├── schemas/      # Pydantic request/response schemas
├── core/         # Configuration, database, security, redis utilities
└── exceptions/   # Domain-specific custom exceptions
```

---

## ⚠️ Concurrency & Data Integrity Model

To eliminate any chance of overbooking, the system enforces **strict pessimistic locking** at the database level.

When a booking request is initiated, the target room row is locked within an atomic transaction:

```python
stmt = select(Rooms).where(Rooms.id == room_id).with_for_update()
```

If two concurrent requests attempt to book the same room at the same millisecond, the second transaction is forced to wait until the first transaction completes (COMMIT or ROLLBACK), ensuring **absolute data consistency**.

---

## ⚙️ Getting Started & Deployment

The deployment pipeline is fully automated using Docker.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/igorber283-code/hotel-booking-api.git
cd hotel-booking-api
```

### 2️⃣ Configure Environment Variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

```ini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=booking_db

POSTGRES_TEST_DB=booking_test

SECRET_KEY=change_me_in_production
ALGORITHM=HS256

REDIS_HOST=redis
REDIS_PORT=6379
```

### 3️⃣ Start the Containers

```bash
docker compose up -d --build
```

> 💡 **Automation Note:**
> The backend container waits for PostgreSQL readiness using `pg_isready`, automatically applies all Alembic migrations (`alembic upgrade head`), and starts the Uvicorn server — no manual steps required.

### 4️⃣ Access the Application

- **Base URL:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs

---

## 🧪 Quality Assurance & Testing

The project includes a fully isolated testing environment with extensive coverage.

### Databases

- `booking_db` — development / production
- `booking_test` — isolated test database

### Run Tests Inside Docker Network

### 1. Prepare the test database (Required only once before the first test run):

```bash
docker compose exec db psql -U postgres -d booking_db -c "CREATE DATABASE booking_test;"
```

### 2. Run the test suite:

```bash
docker compose exec backend pytest
```

### Test Coverage

- Authentication flows (registration, login, token validation)
- Integration tests (FastAPI → PostgreSQL → FastAPI)
- Concurrency stress tests (50+ parallel booking attempts checked for Race Condition)
- Cancellation stress tests (50+ parallel requests for deleting the same booking)
- Validation of pessimistic locking behavior
- Robust Redis mock context ensuring tests remain data-isolated

---

## 📊 API Response Examples

### 1️⃣ User Registration

**POST** `/api/v1/auth/register`

```json
{
  "status": "success",
  "data": {
    "id": 42,
    "email": "developer@example.com"
  }
}
```

### 2️⃣ Hotel Search

**GET** `/api/v1/hotels?location=Moscow&date_from=2026-06-01&date_to=2026-06-10`

```json
[
  {
    "id": 3,
    "name": "Метрополь",
    "location": "Москва, Театральный проезд, 2",
    "rooms_count": 150,
    "available_rooms": 14
  }
]
```

### 3️⃣ Create Booking

**POST** `/api/v1/bookings`

```json
{
  "room_id": 12,
  "date_from": "2026-06-01",
  "date_to": "2026-06-05"
}
```

```json
{
  "booking_id": 1048,
  "room_id": 12,
  "user_id": 42,
  "date_from": "2026-06-01",
  "date_to": "2026-06-05",
  "price_per_night": 6500,
  "total_cost": 26000,
  "total_days": 4,
  "status": "confirmed"
}
```

---

## 📈 Production Roadmap
- [✅] Redis caching layer for hotel search
- [  ] Rate limiting for auth endpoints
- [  ] Background tasks (Celery + Redis) for email notifications
- [  ] Observability: Prometheus & Grafana metrics

---

## 👤 Author

Developed as a **professional portfolio project** with a focus on:

- Asynchronous Python architecture
- High-integrity transactional systems
- Secure, production-ready Docker deployments

