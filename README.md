# Lophoro IMS — Inventory Management System

A web-based Inventory Management System built with Django and PostgreSQL, designed to manage products, orders, procurement, and analytics for a retail business.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [User Roles](#user-roles)
- [Modules Overview](#modules-overview)

---

## Features

- Role-based access control (Admin and Staff)
- Product and category management with image upload
- Real-time stock tracking with movement history
- Sales order management with status workflow
- Invoice generation with PAN number support
- Order return processing
- Supplier and purchase order management
- Supplier price history tracking
- Automated database backup
- Audit logging for all critical actions
- Analytics: ABC Analysis, EOQ Calculation, Sales Trends

---

## Tech Stack

| Layer     | Technology             |
|-----------|------------------------|
| Backend   | Python 3.12, Django 6.0.2 |
| Database  | PostgreSQL             |
| Frontend  | HTML, CSS, JavaScript  |
| ORM       | Django ORM             |
| Auth      | Django Custom User Model |
| Config    | python-dotenv          |

---

## Project Structure

```
LophoroIMS/
├── accounts/        # User authentication, roles, and audit logs
├── catalog/         # Products and categories
├── inventory/       # Stock movement tracking
├── orders/          # Sales orders, invoices, and returns
├── procurement/     # Suppliers and purchase orders
├── analytics/       # ABC analysis, EOQ, and sales trends
├── templates/       # HTML templates
├── static/          # CSS and JavaScript files
├── lophoroims/      # Project settings and URL configuration
├── manage.py
├── requirements.txt
└── .env             # Environment variables (not committed)
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- pip

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/prabeshbastakoti/LophoroIMS.git
cd LophoroIMS
```

2. **Create and activate a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory (see [Environment Variables](#environment-variables)).

5. **Create the database**

Open pgAdmin or psql and create a database named `lophoroims`.

6. **Run migrations**

```bash
python manage.py migrate
```

7. **Create a superuser**

```bash
python manage.py createsuperuser
```

8. **Start the development server**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Environment Variables

Create a `.env` file in the root of the project with the following:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DB_NAME=lophoroims
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

---

## Running the Project

```bash
# Activate virtual environment
.venv\Scripts\activate

# Apply any new migrations
python manage.py migrate

# Run the server
python manage.py runserver
```

---

## User Roles

| Role  | Access                                                                 |
|-------|------------------------------------------------------------------------|
| Admin | Full access — users, products, orders, procurement, analytics, reports |
| Staff | Limited access — view and manage orders and stock                      |

---

## Modules Overview

### Accounts
Handles user registration, login, and role management. Every create, update, and delete action across the system is recorded in an audit log tied to the user who performed it.

### Catalog
Manages product listings and categories. Supports product image upload with automatic resizing to optimize storage.

### Inventory
Tracks stock movements (stock in / stock out) for every product. Provides a real-time view of current stock levels.

### Orders
Manages the full sales order lifecycle — from draft to confirmed or cancelled. Supports invoice generation with PAN number, discount, and payment mode. Handles order returns with restocking.

### Procurement
Manages suppliers and purchase orders. Tracks supplier price history per product over time to support cost analysis.

### Analytics
Provides business intelligence tools:
- **ABC Analysis** — classifies products by revenue contribution (A, B, C tiers)
- **EOQ (Economic Order Quantity)** — calculates optimal reorder quantity per product
- **Sales Trends** — visualises sales patterns over time
