# LOPHOROIMS: INVENTORY AND ORDER MANAGEMENT SYSTEM FOR A PREMIUM DECOR STORE
## Project Report — Part 1 of 4 (Pre-matter + Chapters 1–2)

---

# COVER PAGE

AFFILIATED TO TRIBHUVAN UNIVERSITY
INSTITUTE OF SCIENCE AND TECHNOLOGY

[TU Logo]

A Project Report on

**"LophoroIMS: Inventory and Order Management System for a Premium Decor Store"**

A report submitted for the partial fulfillment of requirements for the degree of
Bachelor of Science in Computer Science and Information Technology
Seventh Semester

**Submitted By:**
Prabesh Bastakoti
Sandesh Poudel
Sudarshan Pandey

**Submitted To:**
Birendra Multiple Campus
Department of Computer Science and Information Technology
Bharatpur-10, Chitwan

May, 2026

---

# SUPERVISOR RECOMMENDATION

This is to certify that this project report entitled **"LophoroIMS: Inventory and Order Management System for a Premium Decor Store"** submitted by Prabesh Bastakoti, Sandesh Poudel, and Sudarshan Pandey has been prepared under my supervision and is submitted in partial fulfillment of the requirements for the degree of Bachelor of Science in Computer Science and Information Technology (BSc CSIT), Seventh Semester, Tribhuvan University.

To the best of my knowledge, this work is original and has not been submitted elsewhere for any academic degree or diploma.

I hereby recommend this project report for evaluation.

**Supervisor:**
[Supervisor Name]
Department of CSIT
Birendra Multiple Campus
Bharatpur-10, Chitwan

Date: _______________

---

# APPROVAL LETTER

This project report entitled **"LophoroIMS: Inventory and Order Management System for a Premium Decor Store"** submitted by Prabesh Bastakoti, Sandesh Poudel, and Sudarshan Pandey has been examined and approved by the following evaluation committee for the partial fulfillment of the requirements of the degree of Bachelor of Science in Computer Science and Information Technology, Seventh Semester, Tribhuvan University.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Head / Program Coordinator | | | |
| Project Supervisor | | | |
| Internal Examiner | | | |
| External Examiner | | | |

---

# ACKNOWLEDGEMENT

We would like to express our sincere gratitude to all those who have contributed to the successful completion of this project.

First and foremost, we extend our deepest appreciation to our project supervisor at Birendra Multiple Campus, Department of Computer Science and Information Technology, for providing invaluable guidance, constructive feedback, and continuous encouragement throughout the development of LophoroIMS. The supervisor's expertise and insights were instrumental in shaping both the technical implementation and academic documentation of this project.

We are equally thankful to the Head and Program Coordinator of the Department of CSIT at Birendra Multiple Campus for their administrative support and for creating an environment that fosters academic and technical growth.

We express our gratitude to the faculty members and internal examiners of the Department of CSIT for their academic inputs during proposal defense and midterm evaluation. Their critical assessments helped us refine the system architecture and analytical components significantly.

Our sincere thanks go to Tribhuvan University, Institute of Science and Technology, for prescribing a curriculum that integrates real-world software engineering practices and project-based learning into the BSc CSIT program.

We also acknowledge the open-source communities behind Python, Django, PostgreSQL, Bootstrap, Chart.js, ReportLab, and openpyxl, whose freely available tools formed the technological foundation of LophoroIMS.

Finally, we are grateful to our families and friends for their patience, moral support, and encouragement throughout the duration of this project.

**Prabesh Bastakoti**
**Sandesh Poudel**
**Sudarshan Pandey**

Birendra Multiple Campus, Bharatpur-10, Chitwan
May, 2026

---

# ABSTRACT

LophoroIMS is a web-based Inventory and Order Management System developed for Lophoro Decor, a premium interior decor store located in Bharatpur-11, Chitwan, Nepal. The system addresses critical operational inefficiencies arising from manual inventory management, including inaccurate stock tracking, absence of demand-based replenishment strategies, and lack of visibility into sales performance.

The system is implemented using the Django web framework (version 6.0.2) with Python as the backend language, PostgreSQL as the relational database, and HTML, CSS, Bootstrap, and JavaScript for the frontend interface. The application follows a Model-View-Template (MVT) architecture and employs a role-based access control mechanism distinguishing between Admin and Staff users.

LophoroIMS integrates three core inventory optimization algorithms: the Economic Order Quantity (EOQ) algorithm for optimal reorder quantity determination, the ABC Classification algorithm for revenue-based product prioritization, and the Sales Trend Analysis algorithm for month-over-month revenue growth computation. These analytical components operate directly on transactional data stored in the PostgreSQL database without reliance on external analytical libraries.

The system encompasses six functional modules: user account management, product and category catalog management, real-time inventory tracking with stock movement audit trails, sales order lifecycle management (including order confirmation, cancellation, and returns), supplier and purchase order management, and a comprehensive analytics and reporting dashboard. Additional features include automated PDF tax invoice generation in Nepalese billing format and data export to Excel and PDF formats.

The development followed an Iterative and Incremental Software Development Life Cycle (SDLC) model across four structured increments, each tested before integration. The system was deployed on a local server environment and validated through unit testing of algorithm implementations and system testing of transactional workflows.

**Keywords:** Inventory Management System, Django, EOQ Algorithm, ABC Classification, Sales Trend Analysis, Role-Based Access Control, PostgreSQL, Web Application

---

# TABLE OF CONTENTS

| Section | Title | Page |
|---------|-------|------|
| | Cover Page | |
| | Supervisor Recommendation | i |
| | Approval Letter | ii |
| | Acknowledgement | iii |
| | Abstract | iv |
| | Table of Contents | v |
| | List of Abbreviations | vii |
| | List of Figures | viii |
| | List of Tables | ix |
| **Chapter 1** | **Introduction** | **1** |
| 1.1 | Introduction | 1 |
| 1.2 | Problem Statement | 3 |
| 1.3 | Objectives | 4 |
| 1.4 | Scope and Limitation | 5 |
| 1.5 | Development Methodology | 6 |
| 1.6 | Report Organization | 9 |
| **Chapter 2** | **Background Study and Literature Review** | **10** |
| 2.1 | Background Study | 10 |
| 2.2 | Literature Review | 17 |
| **Chapter 3** | **System Analysis** | **20** |
| 3.1.1 | Requirement Analysis | 20 |
| 3.1.2 | Feasibility Analysis | 27 |
| 3.1.3 | System Analysis (Structured Approach) | 31 |
| **Chapter 4** | **System Design** | **40** |
| 4.1 | System Design | 40 |
| 4.2 | Algorithm Details | 54 |
| **Chapter 5** | **Implementation and Testing** | **62** |
| 5.1 | Implementation | 62 |
| 5.2 | Testing | 85 |
| 5.3 | Result Analysis | 95 |
| **Chapter 6** | **Conclusion and Future Recommendations** | **97** |
| 6.1 | Conclusion | 97 |
| 6.2 | Future Recommendations | 98 |
| | References | 100 |
| | Appendix A: Screenshots | 102 |
| | Appendix B: Major Source Code Components | 105 |
| | Appendix C: Log of Visits to Supervisor | 120 |

---

# LIST OF ABBREVIATIONS

| Abbreviation | Full Form |
|---|---|
| ABC | Always Better Control |
| API | Application Programming Interface |
| ASGI | Asynchronous Server Gateway Interface |
| CSRF | Cross-Site Request Forgery |
| CSIT | Computer Science and Information Technology |
| CSS | Cascading Style Sheets |
| DB | Database |
| DFD | Data Flow Diagram |
| EOQ | Economic Order Quantity |
| ER | Entity-Relationship |
| FIFO | First In First Out |
| FK | Foreign Key |
| HTML | HyperText Markup Language |
| HTTP | HyperText Transfer Protocol |
| IMS | Inventory Management System |
| JS | JavaScript |
| MVC | Model-View-Controller |
| MVT | Model-View-Template |
| NPR | Nepalese Rupee |
| ORM | Object-Relational Mapping |
| PAN | Permanent Account Number |
| PDF | Portable Document Format |
| PK | Primary Key |
| RBAC | Role-Based Access Control |
| RDBMS | Relational Database Management System |
| SDLC | Software Development Life Cycle |
| SQL | Structured Query Language |
| TU | Tribhuvan University |
| UI | User Interface |
| UML | Unified Modeling Language |
| URL | Uniform Resource Locator |
| WSGI | Web Server Gateway Interface |
| XLS | Excel Spreadsheet |
| XLSX | Excel Open XML Spreadsheet |

---

# LIST OF FIGURES

| Figure No. | Caption | Page |
|---|---|---|
| Figure 1.1 | Iterative and Incremental SDLC Model for LophoroIMS | 7 |
| Figure 2.1 | Django MVT Architecture | 11 |
| Figure 2.2 | EOQ Cost Curve | 14 |
| Figure 2.3 | ABC Classification Pareto Chart | 15 |
| Figure 3.1 | Use Case Diagram of LophoroIMS | 21 |
| Figure 3.2 | DFD Level 0 of LophoroIMS | 33 |
| Figure 3.3 | DFD Level 1 — Inventory and Order Processing | 35 |
| Figure 3.4 | DFD Level 1 — Analytics Processing | 37 |
| Figure 3.5 | Entity-Relationship Diagram of LophoroIMS | 39 |
| Figure 4.1 | Login Page Interface Design | 45 |
| Figure 4.2 | Analytics Dashboard Interface Design | 46 |
| Figure 4.3 | Order Creation Interface with Formset | 47 |
| Figure 4.4 | EOQ Report Interface | 48 |
| Figure 4.5 | ABC Classification Report Interface | 49 |
| Figure 4.6 | Tax Invoice PDF Layout | 50 |
| Figure 4.7 | EOQ Algorithm Flowchart | 55 |
| Figure 4.8 | ABC Classification Algorithm Flowchart | 58 |
| Figure 4.9 | Sales Trend Analysis Algorithm Flowchart | 61 |
| Figure 5.1 | LophoroIMS Module Architecture | 63 |
| Figure 5.2 | Gantt Chart of Development Schedule | 30 |

---

# LIST OF TABLES

| Table No. | Caption | Page |
|---|---|---|
| Table 3.1 | Functional Requirements of LophoroIMS | 22 |
| Table 3.2 | Non-Functional Requirements of LophoroIMS | 26 |
| Table 3.3 | Use Case Description — Login | 22 |
| Table 3.4 | Use Case Description — Manage Product | 23 |
| Table 3.5 | Use Case Description — Manage Inventory | 24 |
| Table 3.6 | Use Case Description — Manage Orders | 24 |
| Table 3.7 | Use Case Description — View Reports | 25 |
| Table 3.8 | Use Case Description — Manage Suppliers | 25 |
| Table 3.9 | Use Case Description — Manage Users | 26 |
| Table 3.10 | Development Schedule (Gantt Chart) | 30 |
| Table 4.1 | Database Table: accounts_user | 41 |
| Table 4.2 | Database Table: accounts_auditlog | 41 |
| Table 4.3 | Database Table: catalog_category | 42 |
| Table 4.4 | Database Table: catalog_product | 42 |
| Table 4.5 | Database Table: inventory_stockmovement | 43 |
| Table 4.6 | Database Table: orders_customer | 43 |
| Table 4.7 | Database Table: orders_order | 44 |
| Table 4.8 | Database Table: orders_orderitem | 44 |
| Table 4.9 | Database Table: orders_orderstatuslog | 44 |
| Table 4.10 | Database Table: orders_orderreturn | 45 |
| Table 4.11 | Database Table: orders_invoice | 45 |
| Table 4.12 | Database Table: procurement_supplier | 46 |
| Table 4.13 | Database Table: procurement_purchase | 46 |
| Table 4.14 | Database Table: procurement_purchaseitem | 47 |
| Table 4.15 | Database Table: procurement_supplierpricehistory | 47 |
| Table 4.16 | EOQ Algorithm Verification with Sample Data | 57 |
| Table 4.17 | ABC Classification Algorithm Verification | 60 |
| Table 5.1 | Tools and Technologies Used | 64 |
| Table 5.2 | Python Packages and Versions | 65 |
| Table 5.3 | Unit Test Cases — EOQ Algorithm | 86 |
| Table 5.4 | Unit Test Cases — ABC Classification | 88 |
| Table 5.5 | Unit Test Cases — Sales Trend Analysis | 90 |
| Table 5.6 | System Test Cases — Authentication | 91 |
| Table 5.7 | System Test Cases — Inventory Operations | 92 |
| Table 5.8 | System Test Cases — Order Lifecycle | 93 |
| Table 5.9 | System Test Cases — Purchase Lifecycle | 94 |
| Table 5.10 | Test Results Summary | 95 |

---

# CHAPTER 1: INTRODUCTION

## 1.1 Introduction

In the contemporary retail landscape, efficient inventory and order management constitute the operational backbone of any product-centric business. Retail enterprises, particularly those dealing with high-value and aesthetically curated products, face unique challenges in maintaining optimal stock levels, accurately recording sales transactions, and making data-driven procurement decisions. The transition from manual or spreadsheet-based inventory management to structured digital systems has become a necessity rather than a luxury for businesses seeking operational efficiency and competitive advantage.

Lophoro Decor is a premium interior decor store located in Bharatpur-11, Chitwan, Nepal, that specializes in high-value decorative items including furniture, wall art, lighting fixtures, and home accessories. As a premium establishment, Lophoro Decor deals with products that carry significant unit costs and are subject to seasonal demand fluctuations. The store serves both walk-in customers and operates through internal staff-managed order processes. Prior to this project, the store managed its inventory through informal manual records and basic spreadsheets, resulting in persistent challenges including inaccurate stock counts, delayed replenishment decisions, and limited visibility into which products drive the most revenue.

LophoroIMS (Lophoro Inventory and Order Management System) is a web-based internal management system developed specifically to address these operational deficiencies. The system is designed as an internal tool accessible exclusively to authenticated Admin and Staff users within the organization, supporting their day-to-day operational workflows across product management, inventory tracking, order recording, supplier management, and business analytics.

The system is built using the Django web framework (version 6.0.2) on the Python programming language, with PostgreSQL serving as the relational database management system. The frontend interface is developed using HTML, CSS, Bootstrap 5, and JavaScript, providing a responsive and intuitive user experience. The application follows Django's Model-View-Template (MVT) architectural pattern, which cleanly separates the data layer (models), business logic layer (views and services), and presentation layer (templates).

A distinguishing characteristic of LophoroIMS is its integration of inventory optimization algorithms directly within the application logic. The Economic Order Quantity (EOQ) algorithm is implemented to compute the optimal purchase quantity for each product, thereby minimizing the combined ordering and holding costs. The ABC Classification algorithm categorizes products based on their cumulative revenue contribution, enabling management to prioritize stock control efforts on high-value items. The Sales Trend Analysis module computes month-over-month revenue patterns from historical confirmed order data, providing actionable insights into product performance and seasonal demand.

The system employs a role-based access control (RBAC) mechanism that distinguishes between two user roles — Admin and Staff. Both roles share access to core operational modules including product management, inventory management, order management, and report viewing. Administrative functions such as supplier management, user account management, and audit log access are restricted to users with the Admin role. This access structure is implemented programmatically through Django view decorators and validated at the login stage by requiring users to explicitly select their role alongside their credentials.

LophoroIMS was developed following an Iterative and Incremental Software Development Life Cycle (SDLC) model, inspired by Agile principles, across four structured development increments. Each increment focused on a distinct functional area of the system — core structure, inventory and orders, supplier and procurement, and analytics — with testing performed before the integration of each increment into the main system.

The practical outcome of this project is a fully functional, role-aware inventory and order management system that replaces manual workflows with structured digital processes, integrates optimization algorithms to support procurement decision-making, and provides exportable analytical reports for management review.

## 1.2 Problem Statement

Lophoro Decor, like many small and medium-sized retail businesses in Nepal, relied on informal manual records and basic spreadsheet tools for managing its inventory and sales orders prior to this project. While such approaches may suffice for very small-scale operations, they present significant operational limitations as business volume grows and product diversity increases.

The specific problems identified through analysis of the store's operational workflow are as follows:

**Inaccurate and Delayed Stock Tracking:** Manual stock records are susceptible to human error during entry and reconciliation. Without an automated system that updates stock counts in real time upon each sales transaction or purchase receipt, discrepancies accumulate over time. This leads to situations where the recorded stock count does not match physical inventory, resulting in either stockouts (when recorded stock appears adequate but physical stock is depleted) or unnecessary reordering (when recorded stock appears lower than actual physical count).

**Absence of Low-Stock Alert Mechanisms:** The store had no systematic mechanism to identify products approaching critically low stock levels. Without automated alerts, replenishment decisions were reactive rather than proactive, leading to stockout situations that resulted in lost sales opportunities.

**No Strategic Product Classification Based on Revenue Contribution:** The store treated all products with equal inventory management priority regardless of their relative contribution to total revenue. In practice, a small subset of products typically accounts for the majority of revenue. Without a structured classification framework such as ABC analysis, inventory management resources — including storage space, ordering frequency, and financial investment — could not be allocated strategically.

**Limited Visibility into Sales Trends and Product Performance:** Without structured aggregation of historical sales data, management lacked the ability to identify patterns in monthly revenue, recognize fast-moving versus slow-moving products, or anticipate seasonal demand variations. This limited the store's capacity to make proactive procurement and pricing decisions.

**No Systematic Reorder Quantity Optimization:** Procurement decisions regarding how much stock to order were based on intuition rather than quantitative analysis. This led to suboptimal order quantities — either ordering too little (increasing ordering frequency and associated costs) or ordering too much (increasing holding costs and tying up working capital).

**Absence of Formal Invoice Generation:** The store lacked a system for generating standardized tax invoices in the format required by Nepalese financial regulations, necessitating manual invoice preparation.

These problems collectively indicate the need for an integrated internal management system that automates stock tracking, provides analytical decision support through EOQ computation and ABC classification, generates sales trend reports, and supports formal invoice generation — all within a secure, role-based access framework.

## 1.3 Objectives

The primary objectives of LophoroIMS are:

1. **To automate real-time stock monitoring and order recording processes** by implementing transactional stock update mechanisms that automatically adjust inventory levels upon order confirmation and purchase receipt.

2. **To implement the Economic Order Quantity (EOQ) algorithm** for optimal reorder quantity calculation, enabling data-driven procurement decisions that minimize total inventory costs by balancing ordering cost and holding cost against annual demand.

3. **To apply ABC Classification** for revenue-based product categorization, enabling management to prioritize inventory control efforts on high-value products that contribute the most to total revenue.

4. **To perform Sales Trend Analysis** for evaluating product performance and monthly revenue patterns, providing management with data-driven insights into seasonal demand variations and growth trajectories.

5. **To generate analytical reports and formal tax invoices** to support cost-efficient, data-driven inventory decisions and comply with Nepalese billing requirements.

## 1.4 Scope and Limitation

### 1.4.1 Scope

The scope of LophoroIMS encompasses the following functional areas:

- **Role-Based Authentication:** Secure login with explicit role selection for Admin and Staff users, with access rights enforced at both the view and template levels.
- **Product and Category Management:** Full CRUD operations for product catalog items including pricing parameters (selling price, unit cost), inventory optimization parameters (annual demand, ordering cost, holding cost), and product image management with automatic resizing.
- **Real-Time Inventory Tracking:** Automated stock updates via transactional service functions upon order confirmation (stock deduction) and purchase receipt (stock addition), with a complete stock movement audit trail.
- **Order Lifecycle Management:** Creation, confirmation, cancellation, and return processing for sales orders, with status transition logging and PDF tax invoice generation.
- **Supplier and Purchase Management:** Supplier profile management, purchase order creation and receipt, and supplier price history tracking (Admin-restricted).
- **Analytical Modules:** EOQ calculation, ABC classification, and sales trend analysis with Chart.js visualizations.
- **Data Export:** Export of inventory, order, purchase, and customer records to Microsoft Excel (.xlsx) and PDF formats.
- **Audit Logging:** Complete action-level audit trail for all CREATE, UPDATE, and DELETE operations, accessible to Admin users.

### 1.4.2 Limitations

- **No Machine Learning Forecasting:** The system employs statistical analysis (EOQ, ABC, trend growth rates) rather than predictive machine learning models such as ARIMA or exponential smoothing.
- **Single-Store Operation:** The system is designed exclusively for internal single-store operations at Lophoro Decor and does not support multi-branch inventory synchronization or real-time distributed inventory management.
- **No Payment Gateway Integration:** The system generates invoices and records payment mode but does not integrate with digital payment gateways such as Khalti or eSewa.
- **No Barcode or QR Code Scanning:** Stock movements are recorded manually through the web interface rather than via barcode scanning hardware.

## 1.5 Development Methodology

LophoroIMS was developed following an **Iterative and Incremental Software Development Life Cycle (SDLC)** model inspired by Agile principles. This methodology was selected because the system consists of clearly separable functional modules that could be developed, tested, and integrated in sequential increments. The iterative nature of the model allowed requirements to be refined progressively based on testing feedback from earlier increments.

The Iterative and Incremental model combines the structured phase discipline of traditional SDLC with the flexibility of iterative refinement. Each iteration passes through the standard phases of planning, analysis, design, implementation, and testing before delivering a working software increment that is integrated into the growing system.

### Phase I: Requirement Analysis

System requirements were identified through analysis of the internal workflows of Lophoro Decor, focusing on how products are managed, how stock levels are tracked, how customer orders are recorded, and how supplier purchases are processed. Both functional requirements (what the system must do) and non-functional requirements (performance, security, data integrity) were documented.

The system was required to: maintain real-time stock records; automatically deduct stock upon order confirmation; automatically increment stock upon purchase receipt; store cost parameters (ordering cost, holding cost, annual demand) for EOQ computation; and retain historical sales data for ABC classification and trend analysis.

### Phase II: System Design

The system design phase produced the following artifacts:
- Entity-Relationship (ER) diagram defining the database schema across 15 entities
- Data Flow Diagram (DFD) at Level 0 and Level 1
- Interface wireframes for key screens
- Algorithm specifications for EOQ, ABC, and Sales Trend Analysis

The system follows a three-tier client-server architecture: the presentation layer (HTML/CSS/Bootstrap/JavaScript templates), the business logic layer (Django views and service modules), and the data layer (PostgreSQL database accessed via Django ORM).

### Phase III: Incremental Implementation

Development proceeded in four structured increments:

**Increment 1 — Core Structure (Weeks 5–7):**
- Custom User model with ADMIN/STAFF roles extending Django's AbstractUser
- Role-based login with dual-role validation
- Product and Category models with full CRUD operations
- Automatic image resizing via Pillow library
- Database schema migration and PostgreSQL configuration

**Increment 2 — Inventory and Order Module (Weeks 8–9):**
- StockMovement model and transactional stock_in / stock_out service functions
- Order, OrderItem, OrderStatusLog, OrderReturn, and Invoice models
- Order lifecycle: DRAFT → CONFIRMED → CANCELLED with automatic stock deduction on confirmation
- Order return processing with automatic stock restoration
- PDF tax invoice generation using ReportLab in Nepalese billing format with amount-in-words conversion

**Increment 3 — Supplier and Procurement Module (Weeks 10–11):**
- Supplier, Purchase, PurchaseItem, and SupplierPriceHistory models
- Purchase lifecycle: DRAFT → RECEIVED with automatic stock addition on receipt
- Supplier price history logging upon each purchase receipt
- Admin-restricted access to supplier management views

**Increment 4 — Analytical Module (Weeks 12):**
- Analytics dashboard with KPI cards, low-stock alerts, and Chart.js visualizations
- EOQ calculation service with real order history demand sourcing
- ABC classification with cumulative percentage computation
- Sales trend analysis with month-over-month growth calculation
- Data export to Excel (openpyxl) and PDF (ReportLab) for inventory, orders, purchases, and customers
- Audit logging module for complete action tracking

### Phase IV: Testing

Each increment was subjected to unit testing before integration. The final integrated system underwent system-level testing including:
- Unit tests for EOQ formula correctness with known mathematical inputs
- Verification of ABC classification thresholds and cumulative percentage logic
- Validation of sales trend growth rate calculations
- System tests for stock accuracy after order and purchase transactions
- Authentication and authorization boundary testing

### Phase V: Deployment and Documentation

The system was deployed on a local development server using Django's built-in development server and PostgreSQL running on localhost. Static files were collected using Django's `collectstatic` management command. Final documentation encompasses system design artifacts, algorithm implementation details, test validation records, and this project report.

**Figure 1.1: Iterative and Incremental SDLC Model for LophoroIMS**
*(See Figure 1.1 — Iterative and Incremental SDLC diagram showing six phases: Planning/Objectives & Scope → Requirement Analysis → System Analysis & Design → Implementation across 4 increments → Testing and Validation → Deployment and Feedback, with continuous iteration arrows)*

### Development Schedule

**Table 3.10: Development Schedule (Gantt Chart)**

| Activity | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | W13 | W14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Requirement Gathering | ██ | ██ | | | | | | | | | | | | |
| System Design | | | ██ | ██ | | | | | | | | | | |
| Iteration 1 Dev | | | | | ██ | ██ | ██ | | | | | | | |
| Iteration 1 Test | | | | | | ██ | ██ | | | | | | | |
| Iteration 2 Dev | | | | | | | | ██ | ██ | | | | | |
| Iteration 2 Test | | | | | | | | ██ | ██ | | | | | |
| Iteration 3 Dev | | | | | | | | | | ██ | ██ | | | |
| Iteration 3 Test | | | | | | | | | | ██ | ██ | | | |
| Iteration 4 Dev | | | | | | | | | | | | ██ | | |
| Integration Testing | | | | | | | | | | | | ██ | | |
| Deployment | | | | | | | | | | | | | ██ | |
| Documentation | | | | | | | | | | | | ██ | ██ | ██ |
| Presentation | | | | | | | | | | | | | | ██ |

**Total Duration: 14 Weeks**

## 1.6 Report Organization

This report is organized into six chapters, each addressing a distinct phase of the software engineering process:

**Chapter 1 — Introduction** presents the background context of the project, identifies the operational problems that motivated LophoroIMS, states the system objectives and scope, describes the development methodology, and outlines the report structure.

**Chapter 2 — Background Study and Literature Review** provides the theoretical foundation for the technologies, architectural patterns, and algorithms used in LophoroIMS. It reviews relevant existing inventory management systems and identifies the gaps that LophoroIMS addresses.

**Chapter 3 — System Analysis** documents the complete requirements analysis including functional and non-functional requirements with use case diagram and descriptions, feasibility analysis across technical, operational, economic, and schedule dimensions, and structured system analysis using Entity-Relationship diagrams and Data Flow Diagrams.

**Chapter 4 — System Design** presents the database design through transformation of the ER diagram into relational tables with normalization, describes the interface and form designs, and provides detailed algorithmic specifications for EOQ, ABC Classification, and Sales Trend Analysis.

**Chapter 5 — Implementation and Testing** documents the tools and technologies used, describes the implementation of each module with key code constructs, presents unit and system test cases with results, and provides a result analysis of the system's performance against requirements.

**Chapter 6 — Conclusion and Future Recommendations** summarizes the achievements of the project, evaluates the extent to which objectives were met, and recommends potential enhancements for future development.

The report concludes with References (IEEE format), followed by Appendices containing system screenshots, major source code components, and the log of supervisor visits.

---

# CHAPTER 2: BACKGROUND STUDY AND LITERATURE REVIEW

## 2.1 Background Study

This section describes the fundamental theories, general concepts, and terminologies that form the technical and domain-specific foundation of LophoroIMS.

### 2.1.1 Inventory Management Systems

An Inventory Management System (IMS) is an information system that tracks the quantity, location, and status of goods held by an organization. For retail businesses, an effective IMS must maintain accurate records of stock available for sale, generate alerts when stock falls below minimum thresholds, record the inflow of goods through purchases, record the outflow of goods through sales, and provide analytical data to support procurement decisions.

In the context of LophoroIMS, inventory is managed at the individual product level. Every product in the catalog carries a `current_stock` field that reflects the real-time quantity available for sale. This field is updated atomically through transactional service functions — `stock_in()` for additions and `stock_out()` for deductions — ensuring that stock counts remain consistent even under concurrent access. Every stock change is recorded as a `StockMovement` entry, creating a permanent audit trail that enables historical analysis of stock flow patterns.

### 2.1.2 Django Web Framework and MVT Architecture

Django is a high-level Python web framework that follows the Model-View-Template (MVT) architectural pattern [4]. The MVT pattern is a variant of the traditional Model-View-Controller (MVC) pattern, adapted for Django's design philosophy.

In the MVT pattern:
- **Model** defines the data structure and handles all database interactions through Django's Object-Relational Mapper (ORM). In LophoroIMS, models such as `Product`, `Order`, `Purchase`, and `StockMovement` represent the core business entities.
- **View** contains the business logic that processes HTTP requests, interacts with models, applies algorithms, and prepares data for rendering. In LophoroIMS, views are organized within six Django applications: `accounts`, `catalog`, `inventory`, `orders`, `procurement`, and `analytics`.
- **Template** defines the HTML presentation layer, using Django's templating language to render dynamic data returned by views. LophoroIMS uses a base template (`base.html`) with a shared sidebar and header, extended by module-specific templates.

Django's ORM provides an abstraction layer that maps Python class definitions to database tables, allowing developers to interact with the database using Python expressions rather than raw SQL. This abstraction, combined with Django's migration system, ensures that schema changes are tracked, versioned, and applied consistently across development and production environments.

LophoroIMS uses Django 6.0.2, which provides built-in support for CSRF protection, session-based authentication, form validation, file upload handling, and the Django Admin interface. The project uses Django's `AbstractUser` extension to add a custom `role` field to the standard user model, enabling the RBAC mechanism.

### 2.1.3 PostgreSQL Relational Database

PostgreSQL is an advanced open-source relational database management system (RDBMS) that supports ACID (Atomicity, Consistency, Isolation, Durability) properties [5]. In LophoroIMS, PostgreSQL serves as the persistent data store for all business entities.

Key PostgreSQL features utilized in LophoroIMS include:
- **Relational Integrity:** Foreign key constraints maintain referential integrity between related tables (e.g., `OrderItem.product` references `catalog_product`).
- **Decimal Precision:** The `NUMERIC(10,2)` data type used for financial fields (`selling_price`, `unit_cost`, `discount`) ensures precise monetary calculations without floating-point rounding errors.
- **Transaction Support:** Combined with Django's `@transaction.atomic` decorator, PostgreSQL's transaction mechanism ensures that compound operations (such as stock deduction + status update during order confirmation) either complete entirely or roll back entirely, preventing partial updates.
- **Aggregate Functions:** PostgreSQL aggregate functions (`SUM`, `COUNT`) combined with Django ORM annotations are used extensively in the analytics module for EOQ demand calculation, ABC revenue aggregation, and monthly trend computation.

### 2.1.4 Economic Order Quantity (EOQ) Algorithm

The Economic Order Quantity (EOQ) model is a classical inventory optimization formula first developed by Ford W. Harris in 1913 and later refined by R.H. Wilson [3]. It determines the optimal order quantity that minimizes total inventory cost, which is the sum of annual ordering cost and annual holding cost.

The EOQ formula is:

**EOQ = √(2DS / H)**

Where:
- **D** = Annual demand (units per year)
- **S** = Ordering cost per order (cost incurred each time a purchase order is placed, including administrative and shipping costs)
- **H** = Annual holding cost per unit (cost of storing one unit for one year, including storage, insurance, and opportunity cost)

**Derivation of Cost Components:**
- Annual ordering cost = (D / EOQ) × S, representing the number of orders placed per year multiplied by the cost per order.
- Annual holding cost = (EOQ / 2) × H, representing the average inventory held (EOQ/2) multiplied by the per-unit holding cost.
- Total inventory cost = (D/EOQ)×S + (EOQ/2)×H, which is minimized when EOQ = √(2DS/H).

**EOQ in LophoroIMS:** The `calculate_eoq()` function in `analytics/services/eoq.py` implements this formula directly. Annual demand is sourced dynamically — first from the last 365 days of confirmed order history using a database aggregate query, then from the manually entered `product.annual_demand` field if no order history exists. The parameters S (ordering cost) and H (holding cost) are stored as product-level attributes in the `catalog_product` table.

### 2.1.5 ABC Classification Algorithm

ABC Classification, also known as the Pareto Principle applied to inventory, is a categorization method that groups products based on their relative contribution to total sales revenue [3]. The classification follows the empirical observation that approximately 20% of items typically account for 80% of total value.

**Classification Thresholds:**
- **Class A:** Products whose cumulative sales value contribution reaches up to 70% of total revenue. These are high-value items requiring tight inventory control, frequent monitoring, and priority stock availability.
- **Class B:** Products whose cumulative contribution falls between 70% and 90%. These require moderate control and periodic review.
- **Class C:** Products whose cumulative contribution falls between 90% and 100%. These are low-value items that can be managed with simpler controls and larger safety stocks.

**ABC in LophoroIMS:** The `build_abc_report()` function in `analytics/services/abc.py` implements this algorithm by: (1) aggregating the total quantity sold per product from confirmed order items using a Django ORM database query; (2) computing each product's sales value as `quantity sold × selling price`; (3) sorting products in descending order of sales value; (4) computing the running cumulative sum as a percentage of total revenue; and (5) assigning A, B, or C class based on the cumulative percentage thresholds.

### 2.1.6 Sales Trend Analysis

Sales Trend Analysis is the process of examining historical sales data over time to identify patterns, growth trajectories, and seasonal variations. In inventory management, trend analysis helps distinguish fast-moving products from slow-moving ones and enables anticipation of future demand based on historical patterns [3].

**Monthly Revenue Growth Rate:**

**Growth% = ((Revenue_current − Revenue_previous) / Revenue_previous) × 100**

A positive growth percentage indicates revenue increase relative to the prior month, while a negative value indicates a decline. This metric helps management evaluate the effectiveness of stocking decisions and identify months with unusual demand patterns.

**Sales Trend in LophoroIMS:** The `build_sales_trend()` function in `analytics/services/trends.py` groups confirmed order items by month using Django's `TruncMonth` database function, computes monthly revenue by summing `quantity × selling_price` for each item within the month, and calculates the month-over-month growth percentage. The results are rendered as line and bar charts using Chart.js on the analytics dashboard and sales trend report page.

### 2.1.7 Role-Based Access Control (RBAC)

Role-Based Access Control (RBAC) is a security mechanism that restricts system access based on the roles assigned to authenticated users. In RBAC, permissions are associated with roles, and users acquire permissions by being assigned to appropriate roles.

In LophoroIMS, two roles are defined — ADMIN and STAFF — using Django's `TextChoices` enumeration on the custom `User` model. The role is enforced at multiple layers:
- **Login validation:** The login view verifies that the submitted role matches the authenticated user's stored role, rejecting credentials where the role selection does not match.
- **View-level decorators:** An `admin_required` decorator wraps sensitive views (supplier management, user management, audit log) and returns an HTTP 403 Forbidden response for non-admin users.
- **Template-level gating:** The navigation sidebar conditionally renders admin-only sections based on the `request.user.role` value.

### 2.1.8 Transactional Stock Operations

In LophoroIMS, all stock-modifying operations are wrapped in Django's `@transaction.atomic` decorator. This ensures that compound operations — such as the sequence of stock deductions performed during order confirmation (one `stock_out()` call per order item) — are treated as a single atomic database transaction. If any individual `stock_out()` call fails (e.g., due to insufficient stock), the entire transaction is rolled back, leaving the database in a consistent state.

This approach guarantees ACID compliance for all inventory-altering operations and prevents scenarios such as partial stock deductions where some items are deducted but others are not due to an error partway through the confirmation process.

### 2.1.9 PDF Generation with ReportLab

ReportLab is a Python library for programmatic PDF document generation. It provides a canvas-based API that allows precise positioning of text, shapes, lines, and tables on A4 or custom-size PDF pages. In LophoroIMS, ReportLab is used in `orders/bill.py` to generate formal tax invoices in Nepalese billing format, including a PAN (Permanent Account Number) display grid, itemized product table with columns for S.N., Particulars, Quantity, Rate (Rs/Ps), and Amount (Rs/Ps), subtotal, discount, tax, and grand total fields, amount-in-words conversion using Indian numbering (ones, tens, hundreds, thousands, lakhs, crores), and staff name signature block.

### 2.1.10 Excel Export with openpyxl

openpyxl is a Python library for reading and writing Microsoft Excel 2010 XLSX files. In LophoroIMS, it is used in `analytics/views.py` to export inventory, order, purchase, and customer records to formatted Excel spreadsheets with styled header rows (brown background, white font matching the application's design system) and appropriate column widths.

## 2.2 Literature Review

This section reviews existing inventory management systems and related research to identify the operational gaps that LophoroIMS addresses.

### 2.2.1 Traditional Manual and Spreadsheet-Based Systems

The majority of small and medium retail businesses in Nepal and similar developing economies continue to rely on manual ledger books or Microsoft Excel spreadsheets for inventory management. While spreadsheets offer familiarity and low cost, they are fundamentally limited as inventory tools. They require manual data entry for every transaction, are prone to formula errors and accidental overwrites, cannot enforce referential integrity across sheets, do not provide real-time concurrent access for multiple staff members, and cannot trigger automated alerts or perform dynamic analytical computations [1].

A study of retail inventory practices in small businesses consistently finds that manual systems lead to stockout frequencies 2–3 times higher than systems with automated reorder notifications, primarily because stock levels are reviewed only periodically rather than updated in real time after each transaction [3]. LophoroIMS directly addresses this by updating `current_stock` atomically upon every confirmed order and received purchase, and by displaying low-stock alerts (products with `current_stock < 10`) prominently on both the dashboard and the inventory current stock view.

### 2.2.2 Enterprise Resource Planning (ERP) Systems

Enterprise-grade inventory management tools such as ERPNext (open-source), SAP Business One, and Oracle NetSuite provide comprehensive, integrated inventory capabilities including multi-warehouse management, barcode scanning, automated reorder triggering, demand forecasting, and financial accounting integration. However, these systems present significant drawbacks for small businesses [2]:

- **Complexity:** Full ERP implementations require extensive configuration, customization, and staff training, often taking months to deploy.
- **Cost:** Even open-source ERPs incur significant implementation, hosting, and maintenance costs.
- **Over-engineering:** Features designed for large enterprises (multi-currency, multi-branch, payroll integration) add complexity without benefit for single-store operations.

LophoroIMS takes a deliberate middle-ground approach — providing the analytical sophistication of EOQ computation and ABC classification that most ERPs include, within a lightweight, purpose-built system designed specifically for Lophoro Decor's single-store internal workflow.

### 2.2.3 Cloud-Based SaaS Inventory Tools

Cloud-based Software-as-a-Service (SaaS) tools such as Zoho Inventory, QuickBooks, and Tally ERP provide subscription-based inventory management with web interfaces. These tools offer real-time stock tracking and sales order management but share several limitations in the context of this project:

- They typically do not expose EOQ computation as a built-in feature; users must calculate reorder quantities manually or purchase add-on modules.
- ABC classification, where available, is often limited to rule-based assignment rather than dynamic computation from transactional sales data.
- SaaS tools incur recurring subscription costs and store business data on third-party servers, raising data privacy concerns for businesses with sensitive supplier and customer information.
- Customization for locale-specific requirements (Nepalese tax invoice format, PAN display, rupee-paisa amount-in-words) is generally not available without significant additional development.

LophoroIMS eliminates subscription costs by using entirely open-source technologies and provides locale-specific invoice generation natively through its `bill.py` module.

### 2.2.4 Academic IMS Projects

Prior BSc CSIT projects at similar institutions have implemented inventory management systems using various technology stacks. Common approaches include PHP/MySQL web applications implementing basic CRUD operations for products and orders, and desktop Java Swing applications with local database files. These systems typically lack analytical modules — EOQ computation and ABC classification are rarely implemented in undergraduate projects due to the additional complexity of dynamic demand sourcing from transactional data [1][2].

LophoroIMS extends the standard IMS scope by implementing EOQ with a dual-source demand strategy (real order history preferred, manual entry as fallback), ABC classification operating on live confirmed order data, and a sales trend module computing growth percentages across historical months. All three algorithms are implemented as pure Python functions without reliance on external analytics libraries such as NumPy or pandas, satisfying the course requirement that students write their own program modules rather than relying on predefined APIs.

### 2.2.5 Summary of Literature Review

The literature review establishes that:

1. Manual and spreadsheet-based systems fail at real-time stock accuracy and provide no analytical decision support.
2. Enterprise ERP systems are over-engineered and cost-prohibitive for single-store SME operations.
3. SaaS tools lack EOQ/ABC integration, impose subscription costs, and cannot meet Nepal-specific invoice formatting requirements.
4. Existing academic IMS projects do not typically implement advanced analytical algorithms.

LophoroIMS addresses all four gaps: it provides real-time automated stock tracking, implements EOQ and ABC algorithms from transactional data, operates cost-free on open-source infrastructure, generates Nepalese-format tax invoices, and implements all algorithmic logic in original Python code without external analytical libraries.
