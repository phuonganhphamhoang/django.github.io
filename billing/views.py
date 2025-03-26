from django.shortcuts import render, redirect
from django.apps import apps
from django.http import JsonResponse
import json
from datetime import datetime
import sqlite3
import pandas as pd
from django.contrib import messages
from django.conf import settings
from .models import BillLine
from django.db import connection

# Hàm chuyển đổi datetime thành chuỗi
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')  # Chuyển datetime thành chuỗi
        return super().default(obj)

def json_view(request):
    all_data = {}

    # Lặp qua tất cả các model trong app 'billing'
    for model in apps.get_app_config('billing').get_models():
        model_name = model.__name__
        all_data[model_name] = list(model.objects.values())

    # Chuyển đổi dữ liệu sang JSON với DateTimeEncoder
    json_data = json.dumps(all_data, cls=DateTimeEncoder)

    return render(request, 'billing/template.html', {'data': json_data})

def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, "❌ Vui lòng chọn một tệp CSV!")
            return redirect('upload_csv')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "❌ File phải là định dạng CSV!")
            return redirect('upload_csv')
        try:
            print("Decode CSV file and load into pandas DataFrame")
            df = pd.read_csv(csv_file)

            # Connect to the SQLite database
            db_path = settings.DATABASES['default']['NAME']  # Django SQLite DB path
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            segments = df[['Mã PKKH', 'Mô tả Phân Khúc Khách hàng']].drop_duplicates()
            for _, row in segments.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO billing_segment (segment_code, segment_info)
                    VALUES (?, ?)
                """, (row['Mã PKKH'], row['Mô tả Phân Khúc Khách hàng']))

            customers = df[['Mã khách hàng', 'Tên khách hàng', 'Mã PKKH']].drop_duplicates()
            for _, row in customers.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO billing_customer (customer_code, customer_name, segment_id)
                    VALUES (?, ?, ?)
                """, (row['Mã khách hàng'], row['Tên khách hàng'], row['Mã PKKH']))

            categories = df[['Mã nhóm hàng', 'Tên nhóm hàng']].drop_duplicates()
            for _, row in categories.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO billing_category (category_code, category_name)
                    VALUES (?, ?)
                """, (row['Mã nhóm hàng'], row['Tên nhóm hàng']))

            products = df[['Mã mặt hàng', 'Tên mặt hàng', 'Mã nhóm hàng', 'Đơn giá']].drop_duplicates()
            for _, row in products.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO billing_product (product_code, product_name, category_id, price)
                    VALUES (?, ?, ?, ?)
                """, (row['Mã mặt hàng'], row['Tên mặt hàng'], row['Mã nhóm hàng'], row['Đơn giá']))

            bills = df[['Mã đơn hàng', 'Mã khách hàng', 'Thời gian tạo đơn']].drop_duplicates()
            for _, row in bills.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO billing_bill (bill_code, customer_id, time_created)
                    VALUES (?, ?, ?)
                """, (row['Mã đơn hàng'], row['Mã khách hàng'], row['Thời gian tạo đơn']))

            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO billing_billline (bill_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (row['Mã đơn hàng'], row['Mã mặt hàng'], row['SL'], row['Đơn giá'], row['Thành tiền']))
            conn.commit()
            conn.close()

            messages.success(request, "✅ Dữ liệu đã được nhập thành công vào SQLite!")
            return redirect(request.META.get('HTTP_REFERER', 'upload_page'))
        except Exception as e:
            messages.error(request, f"❌ Đã xảy ra lỗi: {e}")
            return redirect('upload_csv')

    return render(request, 'billing/upload.html')

# 🔥 Trả dữ liệu về cho D3.js
def visualize_data(request):
    query = """
        SELECT 
            bill.bill_code,
            customer.customer_code,
            product.product_code,
            product.product_name,
            category.category_code,
            category.category_name,
            bill.time_created,
            billline.quantity,
            billline.total_price
        FROM billing_billline AS billline
        INNER JOIN billing_bill AS bill ON billline.bill_id = bill.bill_code
        INNER JOIN billing_customer AS customer ON bill.customer_id = customer.customer_code
        INNER JOIN billing_product AS product ON billline.product_id = product.product_code
        INNER JOIN billing_category AS category ON product.category_id = category.category_code
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    data = [
        {
            "Mã đơn hàng": item[0],
            "Mã khách hàng": item[1],
            "Mã mặt hàng": item[2],
            "Tên mặt hàng": item[3],
            "Mã nhóm hàng": item[4],
            "Tên nhóm hàng": item[5],
            "Thời gian tạo đơn": item[6].strftime('%Y-%m-%d %H:%M:%S') if item[6] else "",
            "SL": item[7],
            "Thành tiền": item[8]
        }
        for item in result
    ]
    return JsonResponse(data, safe=False)

def chart_view(request):
    return render(request, 'billing/chart.html')