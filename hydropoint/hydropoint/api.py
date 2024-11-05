from __future__ import unicode_literals
from xml.etree.ElementTree import tostring
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, comma_and
from collections import defaultdict
from datetime import datetime
from datetime import date
import json 

@frappe.whitelist()
def get_sales_order_details(item_code):
    sales_order_items = frappe.db.sql("""
        SELECT
            so.name AS sales_order_name,
            so.customer AS customer,
            so.transaction_date AS posting_date,
            soi.rate AS item_rate
        FROM
            `tabSales Order` AS so
        INNER JOIN
            `tabSales Order Item` AS soi
        ON
            so.name = soi.parent
        WHERE
            soi.item_code = %(item_code)s
        ORDER BY
            so.transaction_date DESC
        LIMIT 5
    """, {
        'item_code': item_code
    }, as_dict=True)

    # Format the posting_date as dd-mm-yyyy
    for item in sales_order_items:
        item['posting_date'] = item['posting_date'].strftime('%d-%m-%Y')

    return sales_order_items
