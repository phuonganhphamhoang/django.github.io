import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visual.settings')

from django.db import models

# Mô hình Segment
class Segment(models.Model):
    SEGMENT_CODE_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('B3', 'B3'),
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3', 'C3')
    ]

    SEGMENT_INFO_CHOICES = [
        ('A1', 'Nhân viên văn phòng, chủ doanh nghiệp (36-45 tuổi) có mức thu nhập cao, thường xuyên tìm hiểu và quan tâm đến sức khoẻ'),
        ('A2', 'Nhân viên văn phòng, Freelancer ở Miền Bắc (25-35 tuổi) có nhu cầu chăm sóc sức khỏe và quan tâm đến các sản phẩm về trà'),
        ('A3', 'Sinh viên, nhân viên văn phòng, freelancer (18-24 tuổi) có nhu cầu chăm sóc sức khỏe và quan tâm đến sản phẩm về trà'),
        ('B1', 'Người làm kinh doanh hoặc văn phòng (45+ tuổi) có thu nhập trung bình có nhu cầu uống trà để hỗ trợ chữa các bệnh nền'),
        ('B2', 'Người làm nghề nghiệp tự do hoặc nhân viên văn phòng (36-45 tuổi) có nhu cầu uống trà để hỗ trợ chữa các bệnh nền'),
        ('B3', 'Người làm nghề nghiệp tự do hoặc nhân viên văn phòng (25-35 tuổi) ở Miền Bắc có nhu cầu uống trà để hỗ trợ chữa các bệnh có triệu chứng nhẹ'),
        ('C1', 'Sinh viên đi làm thêm, nhân viên mới đi làm (20-29 tuổi) có nhu cầu mua làm quà tặng'),
        ('C2', 'Nhân viên văn phòng, người làm việc tự do (30 - 45 tuổi) ở miền Bắc mua để thử'),
        ('C3', 'Người mua để uống không có mục đích cụ thể (45+)')
    ]  

    segment_code = models.CharField(max_length=50, choices=SEGMENT_CODE_CHOICES, unique=True)
    segment_info = models.CharField(max_length=255, choices=SEGMENT_INFO_CHOICES)

    def __str__(self):
        return self.segment_code

# Mô hình Customer
class Customer(models.Model):
    customer_code = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_code

# Mô hình Category
class Category(models.Model):
    CATEGORY_CODE_CHOICES = [
        ('BOT', 'BOT'),
        ('SET', 'SET'),
        ('THO', 'THO'),
        ('TMX', 'TMX'),
        ('TTC', 'TTC')
    ]

    CATEGORY_NAME_CHOICES = [
        ('BOT', 'Bột'),
        ('SET', 'Set trà'),
        ('THO', 'Trà hoa'),
        ('TMX', 'Trà mix'),
        ('TTC', 'Trà củ, quả sấy')
    ]

    category_code = models.CharField(max_length=50, choices=CATEGORY_CODE_CHOICES, unique=True)
    category_name = models.CharField(max_length=255, choices=CATEGORY_NAME_CHOICES)

    def __str__(self):
        return self.category_code

# Mô hình Product
class Product(models.Model):
    PRODUCT_CODE_CHOICES = [
        ('BOT01', 'BOT01'),
        ('SET01', 'SET01'),
        ('SET02', 'SET02'),
        ('SET03', 'SET03'),
        ('SET04', 'SET04'),
        ('SET05', 'SET05'),
        ('SET06', 'SET06'),
        ('SET07', 'SET07'),
        ('THO01', 'THO01'),
        ('THO02', 'THO02'),
        ('THO03', 'THO03'),
        ('THO04', 'THO04'),
        ('THO05', 'THO05'),
        ('THO06', 'THO06'),
        ('TMX01', 'TMX01'),
        ('TMX02', 'TMX02'),
        ('TMX03', 'TMX03'),
        ('TTC01', 'TTC01'),
        ('TTC02', 'TTC02')
    ]

    PRODUCT_NAME_CHOICES = [
        ('BOT01', 'Bột cần tây'),
        ('SET01', 'Set 10 gói trà nụ hoa nhài trắng'),
        ('SET02', 'Set 10 gói trà hoa đậu biếc'),
        ('SET03', 'Set 10 gói trà hoa cúc trắng'),
        ('SET04', 'Set 10 gói trà gừng'),
        ('SET05', 'Set 10 gói trà dưỡng nhan'),
        ('SET06', 'Set 10 gói trà gạo lứt 8 vị'),
        ('SET07', 'Set 10 gói trà cam sả quế'),
        ('THO01', 'Trà nụ hoa nhài trắng'),
        ('THO02', 'Trà hoa đậu biếc'),
        ('THO03', 'Trà hoa cúc trắng'),
        ('THO04', 'Trà nụ hoa hồng Tây Tạng'),
        ('THO05', 'Trà hoa Atiso'),
        ('THO06', 'Trà nhuỵ hoa nghệ tây'),
        ('TMX01', 'Trà dưỡng nhan'),
        ('TMX02', 'Trà cam sả quế'),
        ('TMX03', 'Trà gạo lứt 8 vị'),
        ('TTC01', 'Trà gừng'),
        ('TTC02', 'Cam lát')
    ]

    product_code = models.CharField(max_length=50, choices=PRODUCT_CODE_CHOICES, unique=True)
    product_name = models.CharField(max_length=255, choices=PRODUCT_NAME_CHOICES)
    price = models.IntegerField() 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_code

# Mô hình Bill
class Bill(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    bill_code = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.bill_code

# Mô hình BillLine
class BillLine(models.Model):
    quantity = models.IntegerField()
    unit_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Line {self.bill} - {self.product}'
    