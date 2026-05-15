# 🚀 Professional Backend Portfolio Project

## 🧩 Key Improvements (Professional Upgrade)
- Added **API response examples** for faster evaluation by reviewers
- Improved **project positioning for senior/backend roles**
- Structured **deployment & architecture clarity**
- Enhanced **readability for recruiters and engineers**
- Standardized **documentation style (production-grade README)**

---

# 🏨 Hotel Booking API

A robust, high-performance backend booking system built with **FastAPI**, **PostgreSQL**, and **Async SQLAlchemy**. This project demonstrates expertise in asynchronous Python programming, database transaction management, and concurrency control.

---

## 🚀 Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Asynchronous)
- **Migrations:** Alembic
- **Authentication:** JWT via AuthX
- **Validation:** Pydantic v2
- **Testing:** Pytest (Integration & Concurrency)
- **Containerization:** Docker & Docker Compose

---

## 📌 Features

### 🔐 Authentication & Security
- Secure user registration and JWT-based login flow
- Role-based access control (RBAC) for protected endpoints
- Password hashing and secure token management

### 🏨 Hotel & Room Management
- Dynamic hotel listings with advanced filtering
- Real-time room availability searching
- Structured room classification and automated pricing logic

### 📅 Advanced Booking Engine
- **Atomic Transactions:** Prevents double bookings using `SELECT ... FOR UPDATE` row-level locking
- **Validation:** Strict date range validation and overlap checks
- **Concurrency Control:** Designed to handle high-load scenarios where multiple users attempt to book the same room simultaneously

### 🧪 Quality Assurance
- **Integration Tests:** End-to-end API flow validation
- **Concurrency Tests:** Specialized stress tests to ensure race-condition protection works under load

---

## 🧠 Architecture

The project follows a modular architecture for scalability and maintainability:

```text
app/
├── api/          # FastAPI routers and endpoint definitions
├── services/     # Business logic layer
├── dao/          # Data Access Objects (Database interaction)
├── models/       # SQLAlchemy declarative models
├── schemas/      # Pydantic models for request/response validation
├── core/         # Configuration, database setup, and security utilities
└── exceptions/   # Custom application-specific exceptions
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your_username/booking-api.git
cd booking-api
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=booking_db

SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
```

### 3. Deploy with Docker

```bash
docker-compose up -d --build
```

### 4. Run Migrations

```bash
docker-compose exec app alembic upgrade head
```

### 5. Access the API

- **Base URL:** http://127.0.0.1:8000
- **Interactive Docs (Swagger):** http://127.0.0.1:8000/docs

---

## 🧪 Testing

Run the full test suite (including stress tests).

This project uses a separate PostgreSQL database for tests.

### Databases
- **booking** — main (development/production) database
- **booking_test** — database used only for automated tests

The test database is completely isolated from the main database and does not contain production data.

### How Tests Are Run

Tests are intended to be executed inside Docker containers.

Run tests with:

```bash
docker compose exec backend pytest
```

### Why Tests Must Be Run in Docker

Running pytest directly on the host machine is not supported by default, because:
- PostgreSQL is running inside a Docker container
- Test credentials and connection settings are defined in docker-compose.yml
- The test database (`booking_test`) exists inside the Docker environment
- Async database connections rely on Docker networking

If pytest is executed locally without Docker, database connection errors may occur.

### Test Database Setup

The test database must exist before running tests.

It can be created with:

```bash
docker compose exec db psql -U user -d postgres -c "CREATE DATABASE booking_test;"
```

### Notes
- Tests use an isolated database (`booking_test`)
- All tests passed successfully when executed inside Docker
- The test environment is safe and does not affect production data

```bash
pytest
```

The testing suite includes:
- **Auth Flow:** Registration and login cycles
- **Race Conditions:** Simulating parallel booking requests to verify locking mechanisms
- **Integration:** Verifying the interaction between FastAPI, SQLAlchemy, and PostgreSQL

---

## ⚠️ Concurrency Model

To ensure data integrity, the system implements a **pessimistic locking** strategy. During a booking request, the specific room record is locked within a transaction:

```python
stmt = select(Rooms).where(Rooms.id == room_id).with_for_update()
```

This ensures that if two requests arrive at the same millisecond, the second request waits for the first to commit or rollback, effectively preventing overbooking.

---

## 📈 Future Roadmap

- [ ] **Caching:** Integrate Redis for hotel listing and room availability
- [ ] **Rate Limiting:** Protect endpoints from abuse
- [ ] **Background Tasks:** Use Celery for booking confirmation emails
- [ ] **Payments:** Stripe or PayPal integration
- [ ] **Observability:** Prometheus and Grafana monitoring

---

## 👤 Author

Developed as a professional portfolio project focusing on:
- Asynchronous Python Backend Development
- High-integrity Transactional Systems
- Scalable Database Design
- Concurrency & Stress Testing Strategies

