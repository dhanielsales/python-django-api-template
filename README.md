# Django REST API Template

A simple Django REST API template with clean architecture, async task processing, and some tools.

## 🚀 Features

- **Django 5.2.2** with **Django REST Framework 3.16.0**
- **Clean Architecture** with Repository and Use Case patterns
- **Celery** integration for async task processing
- **Type Safety** with django-stubs and mypy
- **Automated Testing** with pytest
- **Code Quality** with ruff (linting & formatting)
- **Dependency Management** with uv
- **Database Migrations** with examples
- **Postman Collection** for API testing

## 📋 Prerequisites

- **Python 3.13+**
- **uv** (Python package manager)

## 🛠️ Quick Start

### 1. Setup and Tests

Install dependencies

```bash
uv sync
```

Running tests

```bash
make test
```

### 2. Database Setup

Apply migrations

```bash
make migrate
```

### 3. Run the Application

Start Django development server

```bash
make runserver
```

Start Celery worker (optional)

```bash
make runcelery
```

### 4. Access the API

- **API Base URL**: `http://localhost:8000/api/`
- **Django Admin**: `http://localhost:8000/admin/`

## 📚 API Endpoints

### Deals API

| Method   | Endpoint           | Description            |
| -------- | ------------------ | ---------------------- |
| `GET`    | `/api/deals/`      | List all deals         |
| `POST`   | `/api/deals/`      | Create a new deal      |
| `GET`    | `/api/deals/{id}/` | Get a specific deal    |
| `PUT`    | `/api/deals/{id}/` | Update a specific deal |
| `DELETE` | `/api/deals/{id}/` | Delete a specific deal |

### Example Request

```bash
# Create a deal
curl -X POST http://localhost:8000/api/deals/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Deal",
    "company_id": 1,
    "value": "1000.50",
    "tags": [1, 2],
    "distributor_id": 1
  }'
```

## 🧪 Testing with Postman

Import the provided Postman collection for easy API testing:

1. **Open Postman**
2. **Import Collection**: Use the file `PoCTests.postman_collection.json`
3. **Set Base URL**: Ensure requests point to `http://localhost:8000`
4. **Run Tests**: Execute the collection to test all endpoints

The collection includes:

- ✅ List deals
- ✅ Create deal
- ✅ Get deal by ID
- ✅ Update deal
- ✅ Delete deal

## 🏗️ Project Structure

```
src/
├── config/                # Django settings and configuration
├── core/                  # Django models and core functionality
├── application/
│   ├── presentation/      # API controllers (views)
│   ├── usecase/           # Business logic use cases
│   └── tasks/             # Celery tasks
├── domain/                # Domain entities and interfaces
└── infra/                 # Infrastructure (database, external services)
    ├── db/                # Database repositories
    └── celery/            # Celery configuration
```
