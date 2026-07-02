from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO
from pathlib import Path

from django.conf import settings

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Image, Paragraph, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)

PAN_NUMBER = "126006722"
STORE_NAME = "Lophoro Decor"
STORE_ADDRESS = "Bharatpur-11, Chitwan, Nepal"
THANK_YOU_MSG = "Thank you for your business!"
LOGO_PATH = Path(settings.BASE_DIR) / "static" / "images" / "logo_bill.png"

BLACK = colors.black
DARK = colors.HexColor("#222222")
GREY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#F0F0F0")

# ── Number → Words ────────────────────────────────────────────────────────────

_ONES = [
    '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
    'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
    'Seventeen', 'Eighteen', 'Nineteen',
]
_TENS = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']


def _n2w(n: int) -> str:
    if n == 0:
        return ''
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + (' ' + _ONES[n % 10] if n % 10 else '')
    if n < 1_000:
        return _ONES[n // 100] + ' Hundred' + (' ' + _n2w(n % 100) if n % 100 else '')
    if n < 1_00_000:
        return _n2w(n // 1000) + ' Thousand' + (' ' + _n2w(n % 1000) if n % 1000 else '')
    if n < 1_00_00_000:
        return _n2w(n // 1_00_000) + ' Lakh' + (' ' + _n2w(n % 1_00_000) if n % 1_00_000 else '')
    return _n2w(n // 1_00_00_000) + ' Crore' + (' ' + _n2w(n % 1_00_00_000) if n % 1_00_00_000 else '')


def amount_in_words(amount) -> str:
    amount = Decimal(amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    rupees = int(amount)
    paisa = int((amount - rupees) * 100)
    words = 'Rupees ' + (_n2w(rupees) if rupees else 'Zero')
    if paisa:
        words += f' and {paisa:02d}/100 Paisa'
    return words + ' Only'


# ── Style helpers ─────────────────────────────────────────────────────────────

def _ps(name='Normal', **kwargs) -> ParagraphStyle:
    base = getSampleStyleSheet()[name]
    return ParagraphStyle(f'_custom_{name}_{id(kwargs)}', parent=base, **kwargs)


# ── PAN digit boxes ───────────────────────────────────────────────────────────

def _pan_box_table(pan: str) -> Table:
    digits = list(pan)
    t = Table([digits], colWidths=[0.65 * cm] * len(digits), rowHeights=[0.65 * cm])
    t.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BLACK),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BLACK),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    return t


# ── Main generator ────────────────────────────────────────────────────────────

def generate_bill_pdf(order, invoice_no, bill_date, transaction_date, payment_mode, discount, staff_name) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )
    W = A4[0] - 3 * cm  # usable page width

    elems = []

    # ── 1. Header: Logo + Store ───────────────────────────────────────────────
    logo_cell = ''
    if LOGO_PATH.exists():
        logo_cell = Image(str(LOGO_PATH), width=3 * cm, height=3 * cm, kind='proportional')

    store_p = Paragraph(STORE_NAME, _ps(fontName='Helvetica-Bold', fontSize=16, leading=20))
    addr_p = Paragraph(STORE_ADDRESS, _ps(fontName='Helvetica', fontSize=9, leading=13, textColor=GREY))

    if logo_cell:
        hdr_data = [[logo_cell, [store_p, Spacer(1, 2), addr_p]]]
        hdr_cols = [3.2 * cm, W - 3.2 * cm]
    else:
        hdr_data = [[[store_p, Spacer(1, 2), addr_p]]]
        hdr_cols = [W]

    hdr_t = Table(hdr_data, colWidths=hdr_cols)
    hdr_t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elems.append(hdr_t)
    elems.append(Spacer(1, 0.25 * cm))
    elems.append(HRFlowable(width='100%', thickness=1.2, color=BLACK))
    elems.append(Spacer(1, 0.2 * cm))

    # ── 2. TAX INVOICE title ──────────────────────────────────────────────────
    elems.append(Paragraph('TAX INVOICE', _ps(fontName='Helvetica-Bold', fontSize=15, alignment=TA_CENTER)))
    elems.append(Spacer(1, 0.15 * cm))

    # ── 3. PAN row ────────────────────────────────────────────────────────────
    pan_label = Paragraph('PAN No.:', _ps(fontName='Helvetica-Bold', fontSize=9))
    pan_row = Table(
        [[pan_label, _pan_box_table(PAN_NUMBER)]],
        colWidths=[2 * cm, (0.65 * len(PAN_NUMBER)) * cm],
        hAlign='CENTER',
    )
    pan_row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elems.append(pan_row)
    elems.append(Spacer(1, 0.25 * cm))
    elems.append(HRFlowable(width='100%', thickness=0.6, color=DARK))
    elems.append(Spacer(1, 0.25 * cm))

    # ── 4. Buyer info + Invoice details ──────────────────────────────────────
    lbl = _ps(fontName='Helvetica-Bold', fontSize=8, leading=11)
    val = _ps(fontName='Helvetica', fontSize=9, leading=12)

    customer = order.customer
    buyer_name = customer.name if customer else '—'
    buyer_addr = customer.address if customer else '—'
    buyer_pan = customer.buyer_pan if customer and customer.buyer_pan else '—'

    half = W / 2

    def _kv(k, v):
        return [Paragraph(k, lbl), Paragraph(str(v), val)]

    buyer_t = Table([
        _kv("Buyer's Name:", buyer_name),
        _kv("Address:", buyer_addr),
        _kv("Buyer's PAN:", buyer_pan),
    ], colWidths=[3 * cm, half - 3.2 * cm])
    buyer_t.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    bill_date_str = bill_date.strftime('%Y-%m-%d') if hasattr(bill_date, 'strftime') else str(bill_date)
    txn_date_str = transaction_date.strftime('%Y-%m-%d') if hasattr(transaction_date, 'strftime') else str(transaction_date)

    inv_t = Table([
        _kv("Invoice No.:", invoice_no),
        _kv("Transaction Date:", txn_date_str),
        _kv("Bill Date:", bill_date_str),
        _kv("Payment Mode:", payment_mode),
    ], colWidths=[3.2 * cm, half - 3.4 * cm])
    inv_t.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    info_t = Table([[buyer_t, inv_t]], colWidths=[half, half])
    info_t.setStyle(TableStyle([
        ('BOX', (0, 0), (0, 0), 0.5, DARK),
        ('BOX', (1, 0), (1, 0), 0.5, DARK),
        ('LINEAFTER', (0, 0), (0, 0), 0.5, DARK),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elems.append(info_t)
    elems.append(Spacer(1, 0.3 * cm))

    # ── 5. Items table ────────────────────────────────────────────────────────
    # Columns: S.N. | Particulars | Qty | Rate Rs. | Rate Ps. | Amt Rs. | Amt Ps.
    # Widths must sum to W (18 cm):
    #   1.2 + 7.0 + 1.5 + 2.5 + 1.3 + 2.5 + 2.0 = 18.0
    col_w = [1.2 * cm, 7.0 * cm, 1.5 * cm, 2.5 * cm, 1.3 * cm, 2.5 * cm, 2.0 * cm]
    ih = _ps(fontName='Helvetica-Bold', fontSize=8, alignment=TA_CENTER)
    iv = _ps(fontName='Helvetica', fontSize=8)
    ir = _ps(fontName='Helvetica', fontSize=8, alignment=TA_RIGHT)

    row1 = [
        Paragraph('S.N.', ih),
        Paragraph('Particulars', ih),
        Paragraph('Qty', ih),
        Paragraph('Rate', ih), '',
        Paragraph('Amount', ih), '',
    ]
    row2 = ['', '', '',
            Paragraph('Rs.', ih), Paragraph('Ps.', ih),
            Paragraph('Rs.', ih), Paragraph('Ps.', ih)]

    data = [row1, row2]
    items = list(order.items.select_related('product').all())

    for i, item in enumerate(items, 1):
        rate = item.product.selling_price
        qty = item.quantity
        line_total = (rate * qty).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        r_rs, r_ps = int(rate), round((rate - int(rate)) * 100)
        t_rs, t_ps = int(line_total), round((line_total - int(line_total)) * 100)
        data.append([
            Paragraph(str(i), ir),
            Paragraph(item.product.name, iv),
            Paragraph(str(qty), ir),
            Paragraph(f'{r_rs:,}', ir),
            Paragraph(f'{r_ps:02d}', ir),
            Paragraph(f'{t_rs:,}', ir),
            Paragraph(f'{t_ps:02d}', ir),
        ])

    # Pad to minimum 10 data rows
    while len(data) < 12:
        data.append(['', '', '', '', '', '', ''])

    items_t = Table(data, colWidths=col_w, repeatRows=2)
    items_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#AAAAAA')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Span header row 1 merged cells
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (2, 0), (2, 1)),
        ('SPAN', (3, 0), (4, 0)),
        ('SPAN', (5, 0), (6, 0)),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elems.append(items_t)
    elems.append(Spacer(1, 0.2 * cm))

    # ── 6. Totals ─────────────────────────────────────────────────────────────
    # Align Rs./Ps. columns with the items table Amount columns
    subtotal = sum(
        ((it.product.selling_price * it.quantity) for it in items),
        Decimal('0'),
    ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    disc = Decimal(discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if discount else Decimal('0.00')
    grand_total = subtotal - disc

    def _split(n):
        rs = int(n)
        ps = round((n - rs) * 100)
        return f'{rs:,}', f'{ps:02d}'

    sub_rs, sub_ps = _split(subtotal)
    disc_rs, disc_ps = _split(disc)
    gt_rs, gt_ps = _split(grand_total)

    tl = _ps(fontName='Helvetica', fontSize=9, alignment=TA_RIGHT)
    tb = _ps(fontName='Helvetica-Bold', fontSize=9, alignment=TA_RIGHT)
    tv = _ps(fontName='Helvetica', fontSize=9, alignment=TA_RIGHT)
    tbv = _ps(fontName='Helvetica-Bold', fontSize=9, alignment=TA_RIGHT)

    # left_pad + label(2.5cm) + Rs.(2.5cm) + Ps.(2.0cm) = W
    label_col = W - 2.5 * cm - 2.0 * cm
    tot_col_w = [label_col, 2.5 * cm, 2.0 * cm]

    totals_data = [
        [Paragraph('Sub-Total', tl), Paragraph(sub_rs, tv), Paragraph(sub_ps, tv)],
        [Paragraph('Discount/Others', tl), Paragraph(disc_rs, tv), Paragraph(disc_ps, tv)],
        [Paragraph('Total Taxes', tl), Paragraph('0', tv), Paragraph('00', tv)],
        [Paragraph('Grand Total', tb), Paragraph(gt_rs, tbv), Paragraph(gt_ps, tbv)],
    ]
    totals_t = Table(totals_data, colWidths=tot_col_w)
    totals_t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#AAAAAA')),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elems.append(totals_t)
    elems.append(Spacer(1, 0.3 * cm))

    # ── 7. In Words ───────────────────────────────────────────────────────────
    elems.append(Paragraph(
        f'In Words: <i>{amount_in_words(grand_total)}</i>',
        _ps(fontName='Helvetica-Bold', fontSize=8.5),
    ))
    elems.append(Spacer(1, 0.5 * cm))
    elems.append(HRFlowable(width='100%', thickness=0.6, color=DARK))
    elems.append(Spacer(1, 0.35 * cm))

    # ── 8. Footer ─────────────────────────────────────────────────────────────
    sig_lbl = _ps(fontName='Helvetica', fontSize=8, leading=12)
    sig_name = _ps(fontName='Helvetica-Bold', fontSize=9, leading=13)
    sig_line = _ps(fontName='Helvetica', fontSize=8, textColor=GREY)
    brand = _ps(fontName='Helvetica-Bold', fontSize=11, alignment=TA_CENTER)
    thanks = _ps(fontName='Helvetica-Oblique', fontSize=8, alignment=TA_CENTER, textColor=GREY)

    left_col = [
        Paragraph('Received By:', sig_lbl),
        Spacer(1, 0.7 * cm),
        Paragraph(f'Name: {staff_name}', sig_name),
        Paragraph('________________________________', sig_line),
        Paragraph('Authorized Signature', sig_lbl),
    ]
    right_col = [
        Spacer(1, 0.5 * cm),
        Paragraph(STORE_NAME, brand),
        Spacer(1, 0.2 * cm),
        Paragraph(THANK_YOU_MSG, thanks),
    ]

    footer_t = Table([[left_col, right_col]], colWidths=[W / 2, W / 2])
    footer_t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elems.append(footer_t)

    doc.build(elems)
    buf.seek(0)
    return buf.read()
