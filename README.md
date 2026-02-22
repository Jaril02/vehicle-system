# Vehicle Rental System

A Django project for managing vehicles and bookings, with a web UI and REST API.

---

## Setup steps

1. **Clone or navigate to the project**
   ```bash
   cd "Vehicle system"
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Linux/macOS
   source env/bin/activate
   ```

3. **Environment (optional for local dev)**
   The app runs **without a `.env` file** for local development—it uses a built-in dev secret key. To use your own settings:
   ```bash
   # Windows
   copy .env.example .env
   # Linux/macOS
   cp .env.example .env
   ```
   Edit `.env` and set `SECRET_KEY_VALUE` and any other variables (see [Environment variables](#environment-variables)). **For production, you must set your own `SECRET_KEY_VALUE` in `.env`.**

4. **Install dependencies** (see [Installation](#installation) below).

5. **Run migrations** (see [Migration commands](#migration-commands) below).

6. **Start the server** (see [How to run the project](#how-to-run-the-project) below).

---

## Installation

Install required packages:

```bash
pip install django djangorestframework django-filter python-dotenv
```

Or with a `requirements.txt` in the project root:

```bash
pip install -r requirements.txt
```

**Typical requirements:**

- Django >= 4.0
- djangorestframework
- django-filter
- python-dotenv

---

## Environment variables

The project loads settings from a `.env` file when present (via `python-dotenv`). **You can run the project without `.env`**—a development secret key is used automatically. For production, copy `.env.example` to `.env` and set your own values.

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY_VALUE` | Django secret key (required in production; optional for local dev) | Long random string; see `.env.example` |
| `DEBUG` | Debug mode | `True` or `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |

`.env.example` includes sample/dummy values and commented database options (SQLite by default). Do not commit `.env` to version control.

---

## Migration commands

Create and apply migrations:

```bash
# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

Create a superuser (optional, for admin):

```bash
python manage.py createsuperuser
```

---

## How to run the project

From the project root (where `manage.py` is):

```bash
python manage.py runserver
```

- **Web UI:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **API base:** http://127.0.0.1:8000/api/

---

## How to test APIs

### Using the browser

- **List vehicles:** http://127.0.0.1:8000/api/vehicles/
- **List bookings:** http://127.0.0.1:8000/api/bookings/
- **Filter vehicles:** e.g. http://127.0.0.1:8000/api/vehicles/?brand=Toyota&is_available=true

### Using cURL

**List vehicles**
```bash
curl http://127.0.0.1:8000/api/vehicles/
```

**Create a vehicle**
```bash
curl -X POST http://127.0.0.1:8000/api/vehicles/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Camry\",\"brand\":\"Toyota\",\"year\":2024,\"price_per_day\":\"2500.00\",\"fuel_type\":\"Petrol\",\"is_available\":true}"
```
*(Use `\` instead of `^` on Linux/macOS.)*

**Create a booking** (see [Sample JSON for booking](#sample-json-for-booking) below)
```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ ^
  -H "Content-Type: application/json" ^
  -d "{\"vehicle\":1,\"customer_name\":\"John Doe\",\"customer_phone\":\"9876543210\",\"start_date\":\"2026-03-01\",\"end_date\":\"2026-03-05\"}"
```

### Using Postman or Insomnia

1. Set base URL: `http://127.0.0.1:8000/api/`
2. For POST/PUT, set header: `Content-Type: application/json`
3. Use the [API endpoint list](#api-endpoint-list) and sample JSON below.

---

## API endpoint list

Base URL: **`/api/`**

### Vehicles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vehicles/` | List all vehicles |
| POST | `/api/vehicles/` | Create a vehicle |
| GET | `/api/vehicles/<id>/` | Get vehicle details |
| PUT | `/api/vehicles/<id>/` | Update vehicle |
| PATCH | `/api/vehicles/<id>/` | Partial update |
| DELETE | `/api/vehicles/<id>/` | Delete vehicle |

**Filtering (query params on `GET /api/vehicles/`):**

- `brand=Toyota` — brand (partial match)
- `fuel_type=Electric` — Petrol, Diesel, Electric, Hybrid
- `is_available=true` or `is_available=false`

### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings/` | List all bookings |
| POST | `/api/bookings/` | Create a booking |
| GET | `/api/bookings/<id>/` | Get booking details |
| PUT | `/api/bookings/<id>/` | Update booking |
| PATCH | `/api/bookings/<id>/` | Partial update |
| DELETE | `/api/bookings/<id>/` | Delete booking |

Responses are JSON. For bookings, `total_days` and `total_price` are read-only and set by the server.

---

## Sample JSON for booking

**POST `/api/bookings/`** — create a booking:

```json
{
  "vehicle": 1,
  "customer_name": "John Doe",
  "customer_phone": "9876543210",
  "start_date": "2026-03-01",
  "end_date": "2026-03-05"
}
```

- `vehicle`: ID of an existing vehicle (from `GET /api/vehicles/`).
- `customer_phone`: exactly 10 digits.
- `start_date` / `end_date`: `YYYY-MM-DD`; start must be today or later; end must be after start.
- Vehicle must be available and not already booked for the given dates.

**Example response (201 Created):**

```json
{
  "id": 1,
  "vehicle": 1,
  "customer_name": "John Doe",
  "customer_phone": "9876543210",
  "start_date": "2026-03-01",
  "end_date": "2026-03-05",
  "total_days": 4,
  "total_price": "10000.00"
}
```

**Sample vehicle (POST `/api/vehicles/`):**

```json
{
  "name": "Camry",
  "brand": "Toyota",
  "year": 2024,
  "price_per_day": "2500.00",
  "fuel_type": "Petrol",
  "is_available": true
}
```

---

## Web UI

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Landing with links to vehicles and bookings |
| Vehicles | `/vehicles/` | List with brand, fuel type, and availability filters; add, view, update, delete, book |
| Vehicle detail | `/vehicles/<id>/` | View vehicle; book, update, or delete |
| Add vehicle | `/vehicles/create/` | Create a new vehicle |
| Book vehicle | `/vehicles/<id>/book/` | Create a booking for that vehicle |
| Bookings | `/bookings/` | List all bookings; update or delete each |

Use the navbar to move between Home, Vehicles, and Bookings.
