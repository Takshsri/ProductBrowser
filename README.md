# Product Browser API

## Overview

This project is a backend application built using FastAPI and PostgreSQL to efficiently browse a large product catalog containing 200,000 products.

The application supports category-based filtering and cursor-based pagination to ensure fast and consistent data retrieval even when the dataset is being updated.

## Tech Stack

* Python
* FastAPI
* PostgreSQL (Neon)
* SQLAlchemy
* Faker
* Jinja2
* Uvicorn

## Features

* Generated and stored 200,000 products in PostgreSQL
* Browse products through REST APIs
* Filter products by category
* Cursor-based pagination for efficient navigation
* Database indexing for faster queries
* Simple web interface for viewing products

## Database Design

### Product Table

| Field      | Type        |
| ---------- | ----------- |
| id         | UUID/String |
| name       | String      |
| category   | String      |
| created_at | DateTime    |
| updated_at | DateTime    |

## Data Generation

A seed script was created using the Faker library to generate 200,000 product records. Products are inserted into the database using bulk inserts for better performance.

To generate data:

```bash
python -m app.scripts.seed
```

## API Endpoints

### Get Products

```http
GET /products
```

Query Parameters:

| Parameter         | Description                 |
| ----------------- | --------------------------- |
| limit             | Number of products per page |
| category          | Filter by category          |
| cursor_updated_at | Pagination cursor timestamp |
| cursor_id         | Pagination cursor ID        |

Example:

```http
GET /products?category=Electronics
```

Example with cursor:

```http
GET /products?category=Electronics&cursor_updated_at=2026-07-17T10:38:46&cursor_id=123
```

## Pagination Approach

I chose cursor-based pagination instead of offset pagination.

Offset pagination becomes slower when the dataset grows and may produce duplicate or missing records if new products are inserted while users are browsing.

Cursor pagination uses the last product from the previous page as a reference and provides stable results even when data changes.

Products are ordered using:

```python
Product.updated_at.desc(),
Product.id.desc()
```

The product ID acts as a tie-breaker when multiple products have the same timestamp.

## Database Indexes

The following indexes were added to improve query performance:

```sql
CREATE INDEX idx_products_category
ON products(category);

CREATE INDEX idx_products_updated_id
ON products(updated_at DESC, id DESC);
```

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

Web Interface:

```text
http://127.0.0.1:8000/
```

## Challenges Faced

One of the main challenges was implementing pagination that remains consistent while new products are being added to the database.

To solve this, cursor-based pagination was used along with stable ordering on `updated_at` and `id`.

Another challenge was efficiently inserting 200,000 records. This was handled using bulk insert operations instead of inserting records one by one.

## Future Improvements

* Better frontend interface
* Search by product name
* Sorting options
* Caching frequently accessed results
* Docker deployment

## Author

Developed as part of a backend engineering assignment using FastAPI and PostgreSQL.
