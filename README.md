# Car Inventory API

A simple, and clean **FastAPI + SQLAlchemy** project that provides a RESTful API for managing a basic **Car Inventory System**.
This project demonstrates:
* Well‑structured FastAPI application design
* A relational database schema using SQLAlchemy ORM
* View Owners and Full CRUD operations for Cars
* Automated unit testing with pytest

---

## Features

### **Cars**

* Create a new car
* View all cars or a single car
* Update car details
* Delete a car

### **Owners**

* Create a new owner
* View owners

### **Validation**

* Model year restricted to 100 year range (1925–2025)
* Pydantic models with strict typing

### **Testing**

* Includes unit tests for core API endpoints
* Uses in‑memory SQLite database during tests

---

## Project Structure

```
car-inventory/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD database operations
│   ├── database.py          # DB engine
│   ├── deps.py              # DB session
├── tests/
│   ├── conftest.py          # Test fixtures & setup
│   ├── test_cars.py         # Car API tests
├── requirements.txt
├── README.md                # Project documentation
```

---

## Setup & Run Instructions

### 1. Clone the Project

```bash
git clone <your-repo-url>
cd car-inventory
```

### 2. Create & Activate a Virtual Environment (MacOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available in interactive mode at:

```
http://127.0.0.1:8000/docs
```

### 5. Run Unit Tests

```bash
pytest -s
```

---

## API endpoints along with example cURL API Requests

### Create Owner

```bash
curl -X POST "http://127.0.0.1:8000/owners" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "John Doe",
           "license_number": "A1234567"
         }'
```

### Create Car

```bash
curl -X POST "http://127.0.0.1:8000/cars" \
     -H "Content-Type: application/json" \
     -d '{
           "color": "Red",
           "make": "Toyota",
           "year": 2020,
           "owner_id": 1
         }'
```

### Get All Cars

```bash
curl "http://127.0.0.1:8000/cars"
```

### Update a Car

```bash
curl -X PUT "http://127.0.0.1:8000/cars/1" \
     -H "Content-Type: application/json" \
     -d '{ "color": "Blue" }'
```

### Delete a Car

```bash
curl -X DELETE "http://127.0.0.1:8000/cars/1"
```

---

## Technologies Used

* **FastAPI** — high-performance Python web framework
* **SQLAlchemy ORM** — relational database mapping
* **SQLite** — lightweight local database
* **Pydantic** — data validation
* **Pytest** — automated tests
* **Uvicorn** — ASGI server


---

## Notes

* Code is simple, clean, and easy to extend.
* You can add authentication, pagination, or Docker support if needed.
* It is easier to use the interactive visual mode in web browser to perform the CRUD operations than using the cURL commands in terminal.

## Database Schema (Relational Model)

### **owners** table

| Column         | Type    | Constraints               |
| -------------- | ------- | ------------------------- |
| id             | Integer | Primary key               |
| name           | String  | Not null                  |
| license_number | String  | Unique, indexed, not null |

### **cars** table

| Column   | Type    | Constraints                 |
| -------- | ------- | --------------------------- |
| id       | Integer | Primary key                 |
| color    | String  | Not null                    |
| make     | String  | Not null                    |
| year     | Integer | Range validated (1925–2025) |
| picture  | String  | Optional                    |
| owner_id | Integer | FK → owners.id (required)   |

Relationship:

* One Owner → Many Cars (1:N)

Diagram:

```
owners (1) ────< (N) cars
```

---

## API Endpoints

### **Owner Endpoints**

| Method | Endpoint     | Description          |
| ------ | ------------ | -------------------- |
| POST   | /owners      | Create a new owner   |
| GET    | /owners/{id} | Retrieve owner by ID |

### **Car Endpoints**

| Method | Endpoint   | Description          |
| ------ | ---------- | -------------------- |
| POST   | /cars      | Create a new car     |
| GET    | /cars      | List all cars        |
| GET    | /cars/{id} | Retrieve a car by ID |
| PUT    | /cars/{id} | Update a car         |
| DELETE | /cars/{id} | Delete a car         |

---

## Assumptions & Design Decisions

### **1. SQLite Database**

* Chosen because it is a simple local database.
* Zero configuration; ideal for fast development.

### **2. FastAPI Framework**

* Aligns with modern async Python API development.
* Automatically generates OpenAPI documentation.

### **3. SQLAlchemy ORM**

* Provides clean relational models.
* Ensures safe CRUD operations with session management.

### **4. Data Validation (Pydantic)**

* Car year constrained between **1925–2025** based on realistic historical range.
* Ensures API receives valid, typed inputs.

### **5. Endpoint Structure**

* RESTful conventions followed strictly.
* Separate concerns: CRUD logic in `crud.py`, models in `models.py`, schema validation in `schemas.py`.

### **6. Unit Tests**

* Validated CRUD functionality using an in-memory SQLite DB.
* Ensures reliability and prevents regressions.

---
