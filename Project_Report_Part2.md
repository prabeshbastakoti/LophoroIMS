# LOPHOROIMS PROJECT REPORT — Part 2 of 4 (Chapter 3: System Analysis)

---

# CHAPTER 3: SYSTEM ANALYSIS

## 3.1 System Analysis

System analysis is the phase in which the requirements of the proposed system are examined, categorized, and documented in sufficient detail to support system design. This chapter presents the requirement analysis of LophoroIMS, including functional and non-functional requirements illustrated with a use case diagram and use case descriptions, feasibility analysis across four dimensions, and structured analysis using Entity-Relationship (ER) diagrams and Data Flow Diagrams (DFDs).

## 3.1.1 Requirement Analysis

### i. Functional Requirements

Functional requirements define the specific behaviors and operations that the system must support. The functional requirements of LophoroIMS are derived from the operational workflows of Lophoro Decor and are categorized by module.

**Table 3.1: Functional Requirements of LophoroIMS**

| FR No. | Module | Requirement Description |
|---|---|---|
| FR-01 | Authentication | The system shall allow users to log in by providing a username, password, and role selection (Admin/Staff). |
| FR-02 | Authentication | The system shall reject login attempts where the submitted role does not match the user's stored role. |
| FR-03 | Authentication | The system shall redirect authenticated users to the analytics dashboard upon successful login. |
| FR-04 | Authentication | The system shall allow authenticated users to log out, clearing their session. |
| FR-05 | Product | The system shall allow authorized users to create product records with name, category, selling price, unit cost, EOQ parameters (annual demand, ordering cost, holding cost), current stock, and an optional image. |
| FR-06 | Product | The system shall allow authorized users to edit existing product records. |
| FR-07 | Product | The system shall automatically resize uploaded product images to a maximum of 1000×1000 pixels and compress to JPEG quality 85. |
| FR-08 | Product | The system shall allow authorized users to manage product categories (create, edit). |
| FR-09 | Product | The system shall provide a search facility to find products by name or category. |
| FR-10 | Inventory | The system shall display the current stock level for each product. |
| FR-11 | Inventory | The system shall automatically deduct stock from a product's `current_stock` when a sales order containing that product is confirmed. |
| FR-12 | Inventory | The system shall automatically add stock to a product's `current_stock` when a purchase order containing that product is received. |
| FR-13 | Inventory | The system shall record every stock increment and decrement as a `StockMovement` entry with product, type (IN/OUT), quantity, and timestamp. |
| FR-14 | Inventory | The system shall display a low-stock alert for products with `current_stock` less than 10 units. |
| FR-15 | Order | The system shall allow authorized users to create sales orders with one or more order items (product + quantity), optionally associating a customer record. |
| FR-16 | Order | The system shall support order status transitions: DRAFT → CONFIRMED and DRAFT → CANCELLED. |
| FR-17 | Order | The system shall automatically call `stock_out()` for each order item when a DRAFT order is confirmed. |
| FR-18 | Order | The system shall log every order status change with old status, new status, actor (user), timestamp, and optional note. |
| FR-19 | Order | The system shall allow processing of returns for CONFIRMED orders, restoring the returned quantity to stock. |
| FR-20 | Order | The system shall generate a downloadable PDF tax invoice in Nepalese billing format for confirmed orders, including PAN display, itemized table, subtotal, discount, grand total, and amount in words. |
| FR-21 | Order | The system shall allow authorized users to create and edit customer records with name, phone, email, address, and PAN number. |
| FR-22 | Procurement | The system shall allow Admin users to create and manage supplier records. |
| FR-23 | Procurement | The system shall allow authorized users to create purchase orders with one or more purchase items (product, quantity, unit cost). |
| FR-24 | Procurement | The system shall automatically call `stock_in()` for each purchase item when a DRAFT purchase is received. |
| FR-25 | Procurement | The system shall record the unit cost at time of receipt as a `SupplierPriceHistory` entry for price trend analysis. |
| FR-26 | Analytics | The system shall display a dashboard with KPI cards showing total products, confirmed orders, received purchases, total stock, today's revenue, this month's revenue vs. last month, and pending draft orders. |
| FR-27 | Analytics | The system shall compute EOQ for each product using the formula EOQ = √(2DS/H), sourcing annual demand from real order history where available. |
| FR-28 | Analytics | The system shall classify all products into ABC categories based on cumulative sales value contribution from confirmed orders. |
| FR-29 | Analytics | The system shall compute and display monthly revenue trend with month-over-month growth percentages. |
| FR-30 | Analytics | The system shall export inventory, order, purchase, and customer records to Microsoft Excel (.xlsx) format. |
| FR-31 | Analytics | The system shall export inventory, order, purchase, and customer records to PDF format. |
| FR-32 | Audit | The system shall log all CREATE, UPDATE, and DELETE actions on business objects, recording the acting user, action type, model name, object ID, and timestamp. |
| FR-33 | User Mgmt | Admin users shall be able to create, edit, deactivate, and delete user accounts. |
| FR-34 | User Mgmt | Admin users shall be able to reset any user's password without requiring the old password. |
| FR-35 | User Mgmt | Admin users shall be able to view the last 500 audit log entries. |

### Use Case Diagram

The use case diagram for LophoroIMS identifies two primary actors — Admin and Staff — and seven use cases. Both Admin and Staff can perform Login, Manage Product, Manage Inventory, Manage Orders, and View Reports. Admin additionally has exclusive access to Manage Suppliers and Manage Users.

**Figure 3.1: Use Case Diagram of LophoroIMS**
*(Refer to Figure 3 from the project proposal — Use Case Diagram showing Admin and Staff actors connected to shared use cases: Login, Manage Product, Manage Inventory, Manage Orders, View Reports; Admin-only use cases: Manage Suppliers, Manage Users)*

### Use Case Descriptions

**Table 3.3: Use Case Description — Login**

| Field | Description |
|---|---|
| Use Case Name | Login |
| Actors | Admin, Staff |
| Precondition | User has valid credentials with assigned role |
| Main Flow | 1. User navigates to /accounts/login/. 2. User enters username, password, and selects role (Admin/Staff). 3. System authenticates credentials via Django's `authenticate()`. 4. System verifies submitted role matches user's stored `role` field. 5. System creates session and redirects to /analytics/ dashboard. |
| Alternate Flow | If credentials are invalid: System displays error "Invalid credentials." If role does not match: System displays error "Role does not match account type." |
| Postcondition | User is authenticated and redirected to dashboard. |

**Table 3.4: Use Case Description — Manage Product**

| Field | Description |
|---|---|
| Use Case Name | Manage Product |
| Actors | Admin, Staff |
| Precondition | User is authenticated |
| Main Flow | 1. User navigates to /catalog/products/. 2. System displays all products with category, selling price, unit cost, and current stock. 3. User selects Add Product to create, or Edit to modify an existing record. 4. User submits product form (name, category, selling price, unit cost, EOQ parameters, image). 5. System validates form, saves product record, and resizes uploaded image if provided. |
| Alternate Flow | If form validation fails: System re-renders form with error messages. |
| Postcondition | Product record is created or updated in the database. |

**Table 3.5: Use Case Description — Manage Inventory**

| Field | Description |
|---|---|
| Use Case Name | Manage Inventory |
| Actors | Admin, Staff |
| Precondition | User is authenticated |
| Main Flow | 1. User navigates to /inventory/ to view current stock levels. 2. System displays all products with current stock quantity; highlights products with stock < 10. 3. User navigates to /inventory/movements/ to view stock movement history. 4. System displays all StockMovement records ordered by most recent. |
| Alternate Flow | Stock levels update automatically upon order confirmation or purchase receipt — no manual edit is required from this view. |
| Postcondition | User has viewed current stock and movement history. |

**Table 3.6: Use Case Description — Manage Orders**

| Field | Description |
|---|---|
| Use Case Name | Manage Orders |
| Actors | Admin, Staff |
| Precondition | User is authenticated |
| Main Flow | 1. User navigates to /orders/ to view all orders. 2. User selects Add Order to create a new order. 3. User selects customer (optional) and adds order items (product + quantity) via inline formset. 4. System saves order in DRAFT status. 5. User confirms order from the detail page — system calls `confirm_order()`, which calls `stock_out()` for each item. 6. System logs status transition and updates order to CONFIRMED. 7. User generates PDF invoice by providing invoice details. |
| Alternate Flow | If stock is insufficient during confirmation: System raises ValueError and displays error. User may cancel DRAFT order from detail page. For CONFIRMED orders, user may process returns. |
| Postcondition | Order is confirmed with stock deducted, or cancelled/returned as applicable. |

**Table 3.7: Use Case Description — View Reports**

| Field | Description |
|---|---|
| Use Case Name | View Reports |
| Actors | Admin, Staff |
| Precondition | User is authenticated |
| Main Flow | 1. User navigates to /analytics/ to view dashboard KPIs and charts. 2. User navigates to /analytics/eoq/ for EOQ report. 3. User navigates to /analytics/abc/ for ABC classification report. 4. User navigates to /analytics/trends/ for sales trend analysis. 5. User selects export endpoints to download Excel or PDF reports. |
| Postcondition | User has viewed analytical reports and/or downloaded export files. |

**Table 3.8: Use Case Description — Manage Suppliers**

| Field | Description |
|---|---|
| Use Case Name | Manage Suppliers |
| Actors | Admin only |
| Precondition | User is authenticated with Admin role |
| Main Flow | 1. Admin navigates to /procurement/suppliers/ to view all suppliers. 2. Admin creates or edits supplier records (name, phone, email, address). 3. Admin navigates to /procurement/purchases/ to create purchase orders. 4. Admin creates purchase with supplier, items (product, quantity, unit cost). 5. Admin receives DRAFT purchase — system calls `receive_purchase()`, triggering `stock_in()` for each item and logging `SupplierPriceHistory`. |
| Alternate Flow | Staff users attempting to access supplier management views receive HTTP 403 Forbidden. |
| Postcondition | Supplier records updated; purchase received with stock incremented. |

**Table 3.9: Use Case Description — Manage Users**

| Field | Description |
|---|---|
| Use Case Name | Manage Users |
| Actors | Admin only |
| Precondition | User is authenticated with Admin role |
| Main Flow | 1. Admin navigates to /accounts/users/ to view all user accounts. 2. Admin creates new user (username, role, password). 3. Admin edits user (username, role, active status). 4. Admin resets user password. 5. Admin deletes user (self-deletion is blocked). 6. Admin views audit log at /accounts/audit-log/. |
| Alternate Flow | Staff users attempting to access user management views receive HTTP 403 Forbidden. |
| Postcondition | User accounts updated; audit log reviewed. |

### ii. Non-Functional Requirements

**Table 3.2: Non-Functional Requirements of LophoroIMS**

| NFR No. | Category | Requirement Description |
|---|---|---|
| NFR-01 | Security | All views shall require authentication via Django's `@login_required` decorator. |
| NFR-02 | Security | Admin-only views shall be protected by a custom `admin_required` decorator that returns HTTP 403 for non-admin users. |
| NFR-03 | Security | All state-changing requests (POST/form submissions) shall be protected by Django's CSRF middleware using CSRF tokens. |
| NFR-04 | Security | Passwords shall be stored as hashed values using Django's default PBKDF2-SHA256 password hasher. |
| NFR-05 | Security | Clickjacking attacks shall be mitigated via Django's XFrameOptionsMiddleware. |
| NFR-06 | Data Integrity | All stock-modifying operations shall be wrapped in `@transaction.atomic` to ensure all-or-nothing execution. |
| NFR-07 | Data Integrity | Foreign key constraints shall be enforced at the database level via PostgreSQL. |
| NFR-08 | Data Integrity | Monetary values shall be stored as `NUMERIC(10,2)` to avoid floating-point precision errors. |
| NFR-09 | Performance | List views with related data shall use `select_related()` and `prefetch_related()` to minimize N+1 database query patterns. |
| NFR-10 | Usability | The interface shall be responsive using Bootstrap 5, adapting to desktop, tablet, and mobile viewports. |
| NFR-11 | Usability | User action feedback shall be provided via Django messages framework (success/error/warning toasts). |
| NFR-12 | Maintainability | The codebase shall be organized into six Django apps, each encapsulating a distinct business domain. |
| NFR-13 | Reliability | Database connection parameters shall be configurable via environment variables loaded from a `.env` file using python-dotenv. |

## 3.1.2 Feasibility Analysis

### i. Technical Feasibility

LophoroIMS is technically feasible using the chosen technology stack. Django (version 6.0.2) is a mature, extensively documented web framework with built-in support for authentication, form validation, database migrations, and the admin interface. Python's ecosystem provides all required third-party libraries: ReportLab for PDF generation, openpyxl for Excel export, and Pillow for image processing.

PostgreSQL is a production-grade RDBMS with proven reliability, ACID compliance, and strong support for the decimal precision required in financial calculations. The psycopg2 adapter provides efficient connectivity between Django's ORM and PostgreSQL.

The frontend does not require a complex JavaScript framework; Bootstrap 5 provides sufficient responsive layout capabilities, and Chart.js provides the data visualization components (bar charts for top products, line charts for sales trends, Pareto charts for ABC analysis). All technical dependencies are open-source and widely available.

The development team has practical experience with Python and Django from coursework, making the technology choices technically accessible within the semester timeline.

### ii. Operational Feasibility

LophoroIMS is operationally feasible for Lophoro Decor. The system is designed as an internal web application accessible through any standard web browser, requiring no specialized hardware or software installation on end-user devices. The two-role structure (Admin and Staff) mirrors the existing organizational hierarchy of the store, with role-specific access ensuring that each user can only perform operations appropriate to their responsibilities.

The interface design prioritizes simplicity: the sidebar navigation organizes functionality by logical grouping, form layouts follow familiar web conventions, and contextual alerts (low-stock warnings, draft order notifications) surface critical information proactively. Staff users who are unfamiliar with inventory management software can be trained on basic operations within a short period, given the system's straightforward workflow.

The analytical modules (EOQ, ABC, Sales Trend) reduce the cognitive burden on management by automating computations that would otherwise require manual spreadsheet work, directly supporting more informed procurement decisions.

### iii. Economic Feasibility

The project uses exclusively open-source technologies, eliminating all software licensing costs. The cost breakdown is as follows:

| Component | Technology | Cost |
|---|---|---|
| Web Framework | Django (Python) | Free (BSD License) |
| Database | PostgreSQL | Free (PostgreSQL License) |
| Frontend | Bootstrap 5, Chart.js | Free (MIT License) |
| PDF Generation | ReportLab | Free (BSD License) |
| Excel Export | openpyxl | Free (MIT License) |
| Image Processing | Pillow | Free (HPND License) |
| Development Hardware | Existing laptops | No additional cost |
| Hosting (Development) | Localhost | No additional cost |

Beyond development costs, the system delivers economic value by reducing inventory holding costs through EOQ-guided ordering and by identifying high-revenue products through ABC classification, enabling more focused stock investment. The elimination of stockout-related lost sales further contributes to operational cost efficiency.

### iv. Schedule Feasibility

The 14-week development timeline was structured to accommodate the Iterative and Incremental development approach. Requirement gathering and system design occupied the first four weeks, providing a solid architectural foundation before implementation began. The four development increments — each followed by testing before integration — were completed within weeks 5–12. Integration testing, deployment, documentation, and final presentation occupied the remaining weeks.

The schedule was feasible because: the system's modular architecture allowed parallel team member work across different apps; each increment delivered independently testable functionality; and the technology stack was familiar to team members from prior coursework.

**Table 3.10: Development Schedule is presented in Section 1.5 (Gantt Chart).**

## 3.1.3 Analysis — Structured Approach

LophoroIMS follows the structured analysis approach, using Entity-Relationship (ER) diagrams for data modeling and Data Flow Diagrams (DFDs) for process modeling.

### Entity-Relationship Diagram

The LophoroIMS database comprises 15 entities organized across six Django applications. The following section describes each entity, its attributes, and its relationships with other entities.

**Figure 3.5: Entity-Relationship Diagram of LophoroIMS**
*(The ER diagram shows all 15 entities with their attributes and relationships as described below. Create this diagram using draw.io or Lucidchart based on the entity descriptions.)*

#### Entity Descriptions

**1. User** (accounts_user)
Primary entity representing authenticated system users.
- Attributes: id (PK), username, password (hashed), email, first_name, last_name, role (ADMIN/STAFF), is_active, is_staff, date_joined
- Relationships: One User creates many Orders (created_by); One User creates many Purchases; One User issues many Invoices; One User processes many OrderReturns; One User records many SupplierPriceHistory entries; One User generates many AuditLog entries.

**2. AuditLog** (accounts_auditlog)
Records all system actions for compliance and traceability.
- Attributes: id (PK), user_id (FK→User, nullable), action (CREATE/UPDATE/DELETE), model_name, object_id, object_repr, changes, timestamp
- Relationships: Many AuditLog entries belong to one User (nullable, SET_NULL on user deletion).

**3. Category** (catalog_category)
Lookup table for product classification.
- Attributes: id (PK), name
- Relationships: One Category contains many Products.

**4. Product** (catalog_product)
Core inventory item entity.
- Attributes: id (PK), name, category_id (FK→Category), selling_price, unit_cost, annual_demand, ordering_cost, holding_cost, current_stock, image
- Relationships: Many Products belong to one Category; One Product appears in many OrderItems; One Product appears in many PurchaseItems; One Product appears in many StockMovements; One Product has many SupplierPriceHistory entries; One Product has many OrderReturns.

**5. StockMovement** (inventory_stockmovement)
Immutable audit trail of every stock change.
- Attributes: id (PK), product_id (FK→Product), movement_type (IN/OUT), quantity, created_at
- Relationships: Many StockMovements reference one Product.

**6. Customer** (orders_customer)
Represents customers associated with sales orders.
- Attributes: id (PK), name, phone, email, address, buyer_pan, created_at
- Relationships: One Customer is associated with many Orders (nullable).

**7. Order** (orders_order)
Represents a sales transaction document.
- Attributes: id (PK), customer_id (FK→Customer, nullable), created_by_id (FK→User), created_at, status (DRAFT/CONFIRMED/CANCELLED)
- Relationships: One Order has many OrderItems; One Order has many OrderStatusLogs; One Order has many OrderReturns; One Order has many Invoices.

**8. OrderItem** (orders_orderitem)
Line items within a sales order.
- Attributes: id (PK), order_id (FK→Order), product_id (FK→Product), quantity
- Relationships: Many OrderItems belong to one Order; Many OrderItems reference one Product.

**9. OrderStatusLog** (orders_orderstatuslog)
Immutable history of order status transitions.
- Attributes: id (PK), order_id (FK→Order), old_status, new_status, changed_by_id (FK→User, nullable), changed_at, note
- Relationships: Many OrderStatusLogs belong to one Order; Each log references one User.

**10. OrderReturn** (orders_orderreturn)
Records product return transactions for confirmed orders.
- Attributes: id (PK), order_id (FK→Order), product_id (FK→Product), quantity, reason, returned_at, processed_by_id (FK→User, nullable)
- Relationships: Many OrderReturns belong to one Order; Each references one Product and one User.

**11. Invoice** (orders_invoice)
Formal tax invoice document linked to a confirmed order.
- Attributes: id (PK), order_id (FK→Order), invoice_no (unique), bill_date, transaction_date, payment_mode, discount, staff_name, issued_by_id (FK→User, nullable), issued_at
- Relationships: Many Invoices belong to one Order (typically one per order); Each Invoice references one User as issuer.

**12. Supplier** (procurement_supplier)
Represents product suppliers.
- Attributes: id (PK), name, phone, email, address
- Relationships: One Supplier has many Purchases; One Supplier has many SupplierPriceHistory entries.

**13. Purchase** (procurement_purchase)
Represents a purchase order from a supplier.
- Attributes: id (PK), supplier_id (FK→Supplier), created_by_id (FK→User), created_at, status (DRAFT/RECEIVED/CANCELLED)
- Relationships: One Purchase has many PurchaseItems.

**14. PurchaseItem** (procurement_purchaseitem)
Line items within a purchase order.
- Attributes: id (PK), purchase_id (FK→Purchase), product_id (FK→Product), quantity, unit_cost
- Relationships: Many PurchaseItems belong to one Purchase; Many PurchaseItems reference one Product.

**15. SupplierPriceHistory** (procurement_supplierpricehistory)
Tracks the unit cost charged by each supplier over time per product.
- Attributes: id (PK), supplier_id (FK→Supplier), product_id (FK→Product), unit_cost, recorded_at, recorded_by_id (FK→User, nullable)
- Relationships: Many SupplierPriceHistory entries belong to one Supplier; Many reference one Product.

### Data Flow Diagrams

#### DFD Level 0 (Context Diagram)

The Level 0 DFD represents LophoroIMS as a single process interacting with three external entities: Admin, Staff, and Supplier.

**Figure 3.2: DFD Level 0 of LophoroIMS**

```
                    ┌─────────────────────────────────────────────────────────┐
                    │  Authentication Status, Inventory Reports,               │
         ┌──────────┤  EOQ Results, ABC Results, Sales Trend Analysis          │
         │  Admin   │  User Management Confirmation, Audit Log Data           │
         └──────────┘                     ▲                                    │
                                          │                                    │
    Login Credentials, Product Data,      │                                    │
    Category Data, Supplier Data,         │      ┌──────────────────────────┐ │
    Report Request, User Mgmt Data ───────┼─────►│      LophoroIMS          │ │
                                          │      │  Inventory & Order       │◄┘
    Purchase Order Details ───────────────┤      │  Management System       │
                                          │      └──────────────────────────┘
         ┌──────────┐                     │                 │
         │ Supplier │◄────────────────────┘                 │
         └──────────┘                                       │
    Supply Details, Invoice Information               Authentication Status,
                                                      Order Confirmation,
                                                      Stock Status,
         ┌──────────┐                                  Report Output         │
         │  Staff   │◄─────────────────────────────────────────────────────┘
         └──────────┘
    Login Credentials, Sales Order Data,
    Purchase Order Data, Inventory Update Data,
    Report Request
```

**Data Flows — Admin to LophoroIMS:**
- Login credentials (username, password, role)
- Product data (name, category, pricing, EOQ parameters, image)
- Category data (name)
- Supplier data (name, phone, email, address)
- Purchase order data (supplier, items, unit costs)
- User management data (username, password, role, status)
- Report requests (EOQ, ABC, trends, exports)

**Data Flows — LophoroIMS to Admin:**
- Authentication status (success/failure)
- Inventory reports (current stock, movement history, low-stock alerts)
- EOQ results (optimal order quantities per product)
- ABC classification results (product classifications with cumulative percentages)
- Sales trend analysis (monthly revenue with growth percentages)
- User management confirmations
- Audit log data

**Data Flows — Staff to LophoroIMS:**
- Login credentials (username, password, role)
- Sales order data (customer, order items, quantities)
- Report requests (dashboard, EOQ, ABC, trends, exports)

**Data Flows — LophoroIMS to Staff:**
- Authentication status
- Order confirmation status
- Stock status (current levels, low-stock alerts)
- Report output (dashboard KPIs, analytical reports, PDF invoices, Excel/PDF exports)

**Data Flows — Supplier to LophoroIMS:**
- Purchase order details are recorded by Admin, representing supplier supply information

**Data Flows — LophoroIMS to Supplier:**
- Purchase order details (implicit — purchase records reflect what was ordered from each supplier)

#### DFD Level 1 — Inventory and Order Processing

**Figure 3.3: DFD Level 1 — Inventory and Order Processing**

The Level 1 DFD decomposes the LophoroIMS process into its major sub-processes for inventory and order operations:

```
Process 1.0: User Authentication
   Input:  Login credentials + role selection
   Output: Session token, authentication status
   Data Store: D1 — accounts_user

Process 2.0: Product Management
   Input:  Product data (name, category, pricing, EOQ params, image)
   Output: Product confirmation, updated catalog
   Data Store: D2 — catalog_product, D3 — catalog_category

Process 3.0: Inventory Tracking
   Input:  Stock movement triggers from Process 4.0 (order confirm) and Process 5.0 (purchase receive)
   Output: Updated current_stock, StockMovement record, low-stock alerts
   Data Store: D4 — inventory_stockmovement, D2 — catalog_product (current_stock field)

Process 4.0: Order Management
   Input:  Order data (customer, order items), confirmation/cancellation/return requests
   Sub-processes:
     4.1 Create Order → D5 (orders_order, orders_orderitem)
     4.2 Confirm Order → triggers Process 3.0 (stock_out per item), creates OrderStatusLog
     4.3 Cancel Order → creates OrderStatusLog with note
     4.4 Process Return → triggers Process 3.0 (stock_in), creates OrderReturn
     4.5 Generate Invoice → creates Invoice record, produces PDF output
   Data Store: D5 — orders_order, D6 — orders_orderitem, D7 — orders_orderstatuslog,
               D8 — orders_orderreturn, D9 — orders_invoice

Process 5.0: Procurement Management
   Input:  Supplier data, purchase order data, receive confirmation
   Sub-processes:
     5.1 Manage Supplier → D10 (procurement_supplier)
     5.2 Create Purchase → D11 (procurement_purchase, procurement_purchaseitem)
     5.3 Receive Purchase → triggers Process 3.0 (stock_in per item), creates SupplierPriceHistory
   Data Store: D10 — procurement_supplier, D11 — procurement_purchase,
               D12 — procurement_purchaseitem, D13 — procurement_supplierpricehistory
```

#### DFD Level 1 — Analytics Processing

**Figure 3.4: DFD Level 1 — Analytics Processing**

```
Process 6.0: Analytics and Reporting
   Input:  Report requests from Admin and Staff
   Sub-processes:
     6.1 Dashboard Computation
         → Reads D5 (orders), D11 (purchases), D2 (products)
         → Computes KPIs: total products, confirmed orders, today's revenue,
           this month vs last month revenue, low-stock products
         → Outputs: Dashboard context for Chart.js visualizations

     6.2 EOQ Report
         → For each product in D2:
           Reads last 365 days of D6 (confirmed OrderItems) for demand
           Applies EOQ = √(2DS/H) with product's ordering_cost and holding_cost
         → Outputs: EOQ report table (product, EOQ value, demand source)

     6.3 ABC Classification Report
         → Reads all D6 (confirmed OrderItems) aggregated by product
         → Computes sales_value = qty_sold × selling_price per product
         → Sorts descending by sales_value, computes cumulative %
         → Assigns A (≤70%), B (70–90%), C (>90%) classes
         → Outputs: ABC classification table and Pareto chart data

     6.4 Sales Trend Report
         → Reads D6 (confirmed OrderItems) grouped by TruncMonth
         → Computes monthly revenue = Σ(quantity × selling_price)
         → Computes Growth% = ((current − previous) / previous) × 100
         → Outputs: Monthly trend table and line chart data

     6.5 Data Export
         → Reads D2, D5, D11, orders_customer
         → Generates .xlsx using openpyxl (styled headers, formatted data)
         → Generates .pdf using ReportLab (landscape tables with alternating rows)
         → Outputs: File download responses (HttpResponse with Content-Disposition)
```
