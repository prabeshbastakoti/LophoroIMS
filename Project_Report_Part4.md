# LOPHOROIMS PROJECT REPORT — Part 4 of 4 (Chapter 6 + References + Appendices)

---

# CHAPTER 6: CONCLUSION AND FUTURE RECOMMENDATIONS

## 6.1 Conclusion

LophoroIMS was developed as a web-based internal Inventory and Order Management System for Lophoro Decor, a premium decorative items store located in Bharatpur-11, Chitwan, Nepal. The system was designed to replace manual and spreadsheet-based inventory workflows with a structured digital system that integrates real-time stock tracking, order lifecycle management, procurement management, and analytical decision support.

The project was implemented using Django 6.0.2 (Python) as the backend framework, PostgreSQL as the relational database, and HTML, CSS, Bootstrap 5, and JavaScript (Chart.js) for the frontend interface. The development followed an Iterative and Incremental SDLC model, completing four structured development increments over 14 weeks.

**Achievement of Objectives:**

The first objective — automating real-time stock monitoring and order recording — was fully achieved. The `stock_in()` and `stock_out()` transactional service functions, decorated with `@transaction.atomic`, update the `current_stock` field of the `catalog_product` table atomically upon every order confirmation and purchase receipt respectively. Every stock change is recorded as an immutable `StockMovement` entry, providing a complete and auditable history of all inventory movements. Low-stock alerts for products with stock below 10 units are displayed on both the inventory current stock page and the analytics dashboard.

The second objective — implementing the Economic Order Quantity (EOQ) algorithm — was fully achieved. The `calculate_eoq()` function in `analytics/services/eoq.py` implements the standard EOQ formula (√2DS/H) as a pure Python function. The complementary `get_annual_demand()` function provides a dual-source demand strategy: real confirmed order history from the last 365 days is used when available, with fallback to the manually entered annual demand field. Unit testing validated the algorithm's correctness against manual calculations across 11 test cases with 100% pass rate.

The third objective — applying ABC Classification for revenue-based product categorization — was fully achieved. The `build_abc_report()` function in `analytics/services/abc.py` aggregates confirmed order sales data, computes each product's sales value as quantity sold multiplied by selling price, sorts products by descending sales value, and assigns A, B, or C class based on cumulative revenue contribution thresholds of 70% and 90%. The implementation uses Django ORM database queries and in-memory Python sorting without reliance on external analytics libraries, satisfying the course requirement for original module implementation.

The fourth objective — performing Sales Trend Analysis — was fully achieved. The `build_sales_trend()` function in `analytics/services/trends.py` groups confirmed order items by month using Django's `TruncMonth` database function, computes monthly revenue as the sum of `quantity × selling_price` for all items in each month, and calculates month-over-month growth percentage. The results are presented in a tabular report and visualized as line charts using Chart.js.

The fifth objective — generating analytical reports and formal tax invoices — was fully achieved. The analytics application provides EOQ, ABC, and sales trend report pages with Chart.js visualizations, and exports all major data sets (inventory, orders, purchases, customers) to Microsoft Excel and PDF formats using openpyxl and ReportLab. The `generate_bill_pdf()` function produces PDF tax invoices in the Nepalese billing format, including PAN display, itemized product tables, subtotal, discount, and grand total fields, and amount-in-words conversion using the Indian numbering system.

Additional system capabilities delivered beyond the core five objectives include: role-based access control enforced at login, view, and template levels; a comprehensive audit logging system recording all CREATE, UPDATE, and DELETE actions; customer profile management with PAN numbers for invoice association; order return processing with automatic stock restoration; supplier price history tracking upon each purchase receipt; and a custom CSS design system with responsive layout and JavaScript-driven interactive elements.

**System Validation:** All 50 test cases across unit testing (EOQ, ABC, Sales Trend) and system testing (Authentication, Inventory Operations, Order Lifecycle, Purchase Lifecycle) passed with a 100% success rate, confirming that the system behaves correctly across both individual algorithmic components and integrated end-to-end workflows.

In conclusion, LophoroIMS successfully delivers a functional, analytically capable, and operationally appropriate Inventory and Order Management System for Lophoro Decor. The system addresses all identified problems — inaccurate stock tracking, absence of reorder optimization, lack of product classification, limited sales visibility, and absence of formal invoice generation — through a structured, tested, and documented implementation.

## 6.2 Future Recommendations

While LophoroIMS fulfills its defined scope and meets all stated objectives, several enhancements could significantly extend its capabilities in future development cycles:

**1. Machine Learning-Based Demand Forecasting**
The current EOQ implementation uses annual demand derived from historical order data or manual estimates. Future versions could implement time-series forecasting models such as Moving Average, Exponential Smoothing (Holt-Winters), or ARIMA (AutoRegressive Integrated Moving Average) to predict future demand based on seasonal patterns identified in the sales trend data. This would make EOQ calculations more adaptive to actual demand fluctuations.

**2. Automated Reorder Triggers**
The system currently presents EOQ recommendations passively in a report. A future enhancement could implement automated reorder point (ROP) calculation — ROP = (Average Daily Demand × Lead Time) — and trigger email or in-system notifications when a product's stock falls below its reorder point, enabling proactive rather than reactive procurement.

**3. Barcode and QR Code Integration**
Product identification and stock movement recording currently require manual keyboard entry. Integration with barcode scanner hardware or QR code reading via webcam (using JavaScript libraries such as QuaggaJS) would significantly accelerate stock-in and stock-out operations, reducing data entry errors in warehouse settings.

**4. Multi-Branch Support**
LophoroIMS is designed for single-store operations. Should Lophoro Decor expand to multiple locations, the system could be extended with a Branch model linked to all inventory and order entities, with inter-branch stock transfer capabilities and consolidated reporting across branches.

**5. Payment Gateway Integration**
Future versions could integrate with Nepalese digital payment gateways such as Khalti, eSewa, or IME Pay to enable online payment recording and reconciliation directly within the system, eliminating the need for external payment record-keeping.

**6. Django REST Framework API**
Exposing LophoroIMS functionality through a RESTful API (using Django REST Framework) would enable integration with third-party systems such as accounting software, mobile applications, and e-commerce platforms. This would allow the system to serve as the inventory backbone for a broader digital business infrastructure.

**7. Mobile Application**
A companion mobile application (React Native or Flutter) could enable staff to record stock movements, check current stock levels, and view dashboard KPIs from handheld devices, particularly useful for stockroom operations where desktop access is impractical.

**8. Real-Time Notifications**
Implementing Django Channels (WebSockets) would enable real-time push notifications for critical events such as stock falling below threshold, new orders arriving, or purchases becoming available for receipt — replacing the current approach where users must actively navigate to relevant pages to see alerts.

**9. Comprehensive Reporting Engine**
The current export functionality produces raw data tables. A future reporting engine could generate formatted management reports with charts embedded in PDF documents, scheduled email delivery of daily/weekly summaries, and customizable date-range filtering for all analytical reports.

**10. Advanced Security Features**
Production deployment of LophoroIMS would benefit from two-factor authentication (2FA) for admin accounts, session timeout configuration, IP-based access restrictions, and HTTPS enforcement — all standard requirements for systems handling financial transaction data.

---

# REFERENCES

[1] I. Sommerville, *Software Engineering*, 10th ed. Boston, MA, USA: Pearson Education, 2016.

[2] R. S. Pressman and B. R. Maxim, *Software Engineering: A Practitioner's Approach*, 8th ed. New York, NY, USA: McGraw-Hill, 2015.

[3] W. J. Stevenson, *Operations Management*, 13th ed. New York, NY, USA: McGraw-Hill Education, 2018.

[4] Django Software Foundation, "Django Documentation," 2025. [Online]. Available: https://docs.djangoproject.com/. [Accessed: May 2026].

[5] PostgreSQL Global Development Group, "PostgreSQL Documentation," 2025. [Online]. Available: https://www.postgresql.org/docs/. [Accessed: May 2026].

[6] Bootstrap Team, "Bootstrap Documentation," 2025. [Online]. Available: https://getbootstrap.com/docs/. [Accessed: May 2026].

[7] Python Software Foundation, "Python Documentation," 2025. [Online]. Available: https://docs.python.org/. [Accessed: May 2026].

[8] ReportLab Inc., "ReportLab PDF Library User Guide," 2024. [Online]. Available: https://www.reportlab.com/docs/reportlab-userguide.pdf. [Accessed: May 2026].

[9] openpyxl contributors, "openpyxl Documentation," 2024. [Online]. Available: https://openpyxl.readthedocs.io/. [Accessed: May 2026].

[10] Pillow contributors, "Pillow Documentation," 2025. [Online]. Available: https://pillow.readthedocs.io/. [Accessed: May 2026].

[11] Chart.js contributors, "Chart.js Documentation," 2025. [Online]. Available: https://www.chartjs.org/docs/. [Accessed: May 2026].

[12] F. W. Harris, "How Many Parts to Make at Once," *Factory, The Magazine of Management*, vol. 10, no. 2, pp. 135–136, 1913.

[13] H. A. Taha, *Operations Research: An Introduction*, 10th ed. Upper Saddle River, NJ, USA: Pearson Education, 2017.

---

# APPENDIX A: SCREENSHOTS

*(Note: The following screenshots represent key screens of the LophoroIMS system. Actual screenshots from the running system should be captured and inserted here.)*

**A.1 Login Page**
Screenshot showing the dual-panel login interface: left panel with Lophoro Decor branding and right panel with role toggle (Admin/Staff), username field, password field, and submit button.

**A.2 Analytics Dashboard**
Screenshot showing the dashboard with: total products, confirmed orders, received purchases, and total stock KPI cards; low-stock alert banner (if applicable); today's orders and revenue cards; top 5 products bar chart; monthly revenue trend line chart; and recent orders table.

**A.3 Product List**
Screenshot showing the product catalog table with columns for Product Name, Category, Selling Price (NPR), Unit Cost (NPR), and Current Stock, with Edit action buttons.

**A.4 Product Form**
Screenshot showing the product creation/edit form with fields for name, category, selling price, unit cost, annual demand, ordering cost, holding cost, current stock, and image upload widget.

**A.5 Current Stock Page**
Screenshot showing the inventory current stock table with product names, categories, and stock quantities. Products with stock below 10 units are highlighted with a warning indicator.

**A.6 Stock Movement Log**
Screenshot showing the stock movement history table with columns for Product, Movement Type (IN/OUT badge), Quantity, and Timestamp, ordered by most recent.

**A.7 Order List**
Screenshot showing the orders table with Order #, Customer, Created By, Date, Status badge (Draft/Confirmed/Cancelled), and action links.

**A.8 Order Creation Form**
Screenshot showing the order creation form with customer dropdown and inline order items formset (product dropdown, quantity input, delete checkbox per row).

**A.9 Order Detail Page**
Screenshot showing the complete order detail view with order summary, order items table, status transition log timeline, returns list (if any), invoices list (if any), and action buttons (Confirm/Cancel/Generate Bill).

**A.10 Tax Invoice PDF**
Screenshot of a generated tax invoice PDF showing store header (Lophoro Decor, address, PAN grid), itemized product table, financial summary (subtotal, discount, grand total), amount in words, and signature block.

**A.11 EOQ Report**
Screenshot showing the EOQ report table with columns for Product, Annual Demand, Demand Source (orders/manual/none), Ordering Cost, Holding Cost, and Calculated EOQ quantity.

**A.12 ABC Classification Report**
Screenshot showing the ABC report table with Product, Qty Sold, Sales Value (NPR), Cumulative %, and ABC Class columns, with A/B/C class color-coded badges.

**A.13 Sales Trend Report**
Screenshot showing the monthly sales trend table with Month, Revenue (NPR), and Growth % columns, alongside a line chart of monthly revenue over time.

**A.14 Supplier Management (Admin)**
Screenshot showing the supplier list and supplier creation form accessible to Admin users only.

**A.15 User Management (Admin)**
Screenshot showing the user list with username, role, and active status, along with the user creation and password reset forms.

**A.16 Audit Log (Admin)**
Screenshot showing the audit log table with User, Action (CREATE/UPDATE/DELETE), Model, Object, and Timestamp columns.

---

# APPENDIX B: MAJOR SOURCE CODE COMPONENTS

## B.1 Inventory Service Functions (`inventory/services.py`)

```python
from django.db import transaction
from catalog.models import Product
from .models import StockMovement


@transaction.atomic
def stock_in(product: Product, qty: int) -> StockMovement:
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")

    movement = StockMovement.objects.create(
        product=product,
        movement_type="IN",
        quantity=qty,
    )

    product.current_stock += qty
    product.save(update_fields=["current_stock"])

    return movement


@transaction.atomic
def stock_out(product: Product, qty: int) -> StockMovement:
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")

    if product.current_stock < qty:
        raise ValueError("Not enough stock")

    movement = StockMovement.objects.create(
        product=product,
        movement_type="OUT",
        quantity=qty,
    )

    product.current_stock -= qty
    product.save(update_fields=["current_stock"])

    return movement
```

## B.2 Order Service Functions (`orders/services.py`)

```python
from django.db import transaction
from inventory.services import stock_in, stock_out
from .models import Order, OrderReturn, OrderStatusLog


@transaction.atomic
def confirm_order(order: Order, changed_by=None) -> Order:
    if order.status != "DRAFT":
        raise ValueError("Only DRAFT orders can be confirmed")

    for item in order.items.select_related("product").all():
        stock_out(item.product, item.quantity)

    old_status = order.status
    order.status = "CONFIRMED"
    order.save(update_fields=["status"])
    OrderStatusLog.objects.create(
        order=order, old_status=old_status,
        new_status="CONFIRMED", changed_by=changed_by
    )
    return order


@transaction.atomic
def cancel_order(order: Order, changed_by=None, note="") -> Order:
    if order.status != "DRAFT":
        raise ValueError("Only DRAFT orders can be cancelled")

    old_status = order.status
    order.status = "CANCELLED"
    order.save(update_fields=["status"])
    OrderStatusLog.objects.create(
        order=order, old_status=old_status,
        new_status="CANCELLED", changed_by=changed_by, note=note
    )
    return order


@transaction.atomic
def process_return(order: Order, product, quantity: int,
                   reason: str, processed_by=None) -> OrderReturn:
    if order.status != "CONFIRMED":
        raise ValueError("Returns can only be processed for confirmed orders")

    stock_in(product, quantity)
    return OrderReturn.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        reason=reason,
        processed_by=processed_by,
    )
```

## B.3 Procurement Service Function (`procurement/services.py`)

```python
from django.db import transaction
from inventory.services import stock_in
from .models import Purchase, SupplierPriceHistory


@transaction.atomic
def receive_purchase(purchase: Purchase, received_by=None) -> Purchase:
    if purchase.status != "DRAFT":
        raise ValueError("Only DRAFT purchases can be received")

    for item in purchase.items.select_related("product").all():
        stock_in(item.product, item.quantity)
        SupplierPriceHistory.objects.create(
            supplier=purchase.supplier,
            product=item.product,
            unit_cost=item.unit_cost,
            recorded_by=received_by,
        )

    purchase.status = "RECEIVED"
    purchase.save(update_fields=["status"])
    return purchase
```

## B.4 EOQ Algorithm (`analytics/services/eoq.py`)

```python
import math
from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from catalog.models import Product
from orders.models import OrderItem


def get_annual_demand(product: Product) -> tuple:
    """
    Returns (demand: int, source: str).
    Tries real order history first (last 365 days of confirmed orders).
    Falls back to the manually-entered product.annual_demand if no sales data.
    source is one of: 'orders' | 'manual' | 'none'
    """
    cutoff = timezone.now() - timedelta(days=365)
    result = (
        OrderItem.objects
        .filter(
            order__status='CONFIRMED',
            order__created_at__gte=cutoff,
            product=product,
        )
        .aggregate(total=Sum('quantity'))
    )
    total = result['total'] or 0
    if total > 0:
        return total, 'orders'
    if product.annual_demand > 0:
        return product.annual_demand, 'manual'
    return 0, 'none'


def calculate_eoq(product: Product, annual_demand: int = None):
    D = annual_demand if annual_demand is not None else product.annual_demand
    S = float(product.ordering_cost)
    H = float(product.holding_cost)

    if D <= 0 or S <= 0 or H <= 0:
        return None

    return round(math.sqrt((2 * D * S) / H), 2)
```

## B.5 ABC Classification Algorithm (`analytics/services/abc.py`)

```python
from decimal import Decimal
from django.db.models import Sum
from catalog.models import Product
from orders.models import OrderItem


def build_abc_report():
    """
    Returns list of rows with:
    product, qty_sold, sales_value, cumulative_pct, abc_class
    """
    qs = (
        OrderItem.objects
        .filter(order__status="CONFIRMED")
        .values("product")
        .annotate(qty_sold=Sum("quantity"))
    )

    qty_map = {row["product"]: row["qty_sold"] or 0 for row in qs}

    rows = []
    total_value = Decimal("0")

    for p in Product.objects.all():
        qty = int(qty_map.get(p.id, 0))
        value = (Decimal(qty) * (p.selling_price or Decimal("0"))).quantize(
            Decimal("0.01"))
        rows.append({
            "product": p,
            "qty_sold": qty,
            "sales_value": value,
        })
        total_value += value

    rows.sort(key=lambda r: r["sales_value"], reverse=True)

    running = Decimal("0")
    for r in rows:
        running += r["sales_value"]
        if total_value > 0:
            cumulative_pct = (running / total_value) * Decimal("100")
        else:
            cumulative_pct = Decimal("0")

        if cumulative_pct <= 70:
            abc_class = "A"
        elif cumulative_pct <= 90:
            abc_class = "B"
        else:
            abc_class = "C"

        r["cumulative_pct"] = cumulative_pct.quantize(Decimal("0.01"))
        r["abc_class"] = abc_class

    return rows, total_value.quantize(Decimal("0.01"))
```

## B.6 Sales Trend Analysis (`analytics/services/trends.py`)

```python
from collections import OrderedDict
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from orders.models import OrderItem


def build_sales_trend():
    """
    Returns list of rows:
    month_label, revenue, growth_pct
    """
    items = (
        OrderItem.objects
        .filter(order__status="CONFIRMED")
        .select_related("product")
        .annotate(month=TruncMonth("order__created_at"))
        .order_by("month")
    )

    revenue_by_month = OrderedDict()

    for it in items:
        month = it.month
        if month not in revenue_by_month:
            revenue_by_month[month] = Decimal("0")
        revenue_by_month[month] += (Decimal(it.quantity) * it.product.selling_price)

    rows = []
    prev_rev = None

    for month, rev in revenue_by_month.items():
        rev = rev.quantize(Decimal("0.01"))
        if prev_rev is None or prev_rev == 0:
            growth = None
        else:
            growth = ((rev - prev_rev) / prev_rev) * Decimal("100")
            growth = growth.quantize(Decimal("0.01"))

        rows.append({
            "month": month.strftime("%Y-%m"),
            "revenue": rev,
            "growth": growth,
        })
        prev_rev = rev

    return rows
```

## B.7 User Model and Audit Log (`accounts/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"

    role = models.CharField(
        max_length=10, choices=Roles.choices, default=Roles.STAFF)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_admin(self):
        return self.role == "ADMIN"


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="audit_logs")
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    object_repr = models.CharField(max_length=255)
    changes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return (f"{self.user} {self.action} {self.model_name} "
                f"#{self.object_id} at {self.timestamp:%Y-%m-%d %H:%M}")
```

## B.8 Product Model with Image Resizing (`catalog/models.py`)

```python
from django.db import models
from PIL import Image

MAX_IMAGE_SIZE = (1000, 1000)
IMAGE_QUALITY = 85


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    annual_demand = models.IntegerField(default=0)
    ordering_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._resize_image()

    def _resize_image(self):
        try:
            img = Image.open(self.image.path)
            if img.width > MAX_IMAGE_SIZE[0] or img.height > MAX_IMAGE_SIZE[1]:
                img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(self.image.path, format="JPEG",
                         quality=IMAGE_QUALITY, optimize=True)
        except Exception:
            pass
```

---

# APPENDIX C: LOG OF VISITS TO SUPERVISOR

*(This log should be maintained throughout the project and signed by both the student and supervisor at each visit. A representative format is shown below.)*

| Visit No. | Date | Duration | Topics Discussed | Technical Feedback Received | Student Signature | Supervisor Signature |
|---|---|---|---|---|---|---|
| 01 | Week 2 | 1 hour | Initial requirement discussion; identification of core modules; technology stack selection | Confirmed Django + PostgreSQL stack; recommended EOQ as primary algorithm | | |
| 02 | Week 4 | 1 hour | System design review; ER diagram walkthrough; DFD Level 0 review | Suggested adding AuditLog model for traceability; confirmed use case diagram structure | | |
| 03 | Week 6 | 1.5 hours | Increment 1 demo: User authentication, product management | Feedback: add role mismatch error at login; confirmed image resizing approach | | |
| 04 | Week 8 | 1.5 hours | Increment 2 demo: Inventory tracking, order lifecycle | Feedback: use @transaction.atomic on all stock operations; add OrderStatusLog for audit trail | | |
| 05 | Week 10 | 1 hour | Increment 3 demo: Supplier management, purchase receipt | Feedback: add SupplierPriceHistory for price tracking; review admin_required decorator | | |
| 06 | Week 12 | 2 hours | Increment 4 demo: Full analytics module (EOQ, ABC, trends, exports) | Feedback: document demand sourcing strategy; verify ABC cumulative threshold logic | | |
| 07 | Week 13 | 1 hour | Integration testing review; PDF invoice generation demo | Confirmed test case structure; recommended additional boundary test cases for ABC | | |
| 08 | Week 14 | 1 hour | Final report review; presentation preparation | Feedback: ensure all figures are numbered and captioned; verify IEEE referencing format | | |

*(Actual visit dates, specific feedback details, and signatures should be filled in based on the real supervision log maintained during the project.)*

---

# END OF REPORT

**Report Title:** LophoroIMS: Inventory and Order Management System for a Premium Decor Store

**Submitted By:** Prabesh Bastakoti | Sandesh Poudel | Sudarshan Pandey

**Institution:** Birendra Multiple Campus, Department of CSIT, Bharatpur-10, Chitwan

**Affiliated To:** Tribhuvan University, Institute of Science and Technology

**Submission Date:** May 2026

**Degree:** Bachelor of Science in Computer Science and Information Technology (BSc CSIT), Seventh Semester

---

*Report Format Note for Final Submission:*
*- Paper size: A4*
*- Margins: Top=1in, Bottom=1in, Left=1.25in, Right=1in*
*- Font: Times New Roman, 12pt for body*
*- Line spacing: 1.5*
*- Chapter headings: 16pt bold; Section headings: 14pt bold; Sub-section: 12pt bold*
*- All paragraphs: Justified alignment*
*- Figure captions: Centered below figure, 12pt bold*
*- Table captions: Centered above table, 12pt bold*
*- Page numbering: Roman numerals (i, ii...) for pre-matter; Arabic numerals (1, 2...) from Chapter 1*
*- Page numbers: Bottom, center*
*- Binding: Golden Embracing with Black Binding, 3 copies*
*- IEEE referencing style throughout*
