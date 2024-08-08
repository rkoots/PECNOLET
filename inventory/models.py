from django.db import models
from django.utils import timezone

class Stock(models.Model):
    TYPES = [
        ('electronics', 'Electronics'),
        ('infrastructure', 'Infrastructure'),
        ('custom_machinery', 'Custom Machinery'),
        ('Others', 'Others'),
    ]
    MATERIAL = [
        ('Steel','Steel'),
        ('Aluminum','Aluminum'),
        ('Plastics','Plastics'),
        ('Chemicals','Chemicals'),
        ('Iron','Iron'),
    ]
    PACKING = [
        ('Boxes','Boxes'),
        ('wrapping ','wrapping '),
        ('pallets','pallets'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, verbose_name='Name')
    desc = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    type = models.CharField(max_length=50, choices=TYPES)
    materials = models.CharField(max_length=50, choices=MATERIAL)
    packing = models.CharField(max_length=50, choices=PACKING)
    lotsize = models.IntegerField(default=1)
    file = models.FileField(upload_to='stock_files/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name



class Customer(models.Model):
    BUSINESS_TYPES = [
        ('electronics', 'Electronics'),
        ('infrastructure', 'Infrastructure'),
        ('custom_machinery', 'Custom Machinery'),
        ('Others', 'Others'),
    ]
    INDUSTRY_CHOICES = [
        (75, 'Aerospace and aviation industry'),
        (73, 'Air conditioning, refrigeration and ventilation industry'),
        (56, 'Apparatus engineering'),
        (58, 'Automation and control engineering'),
        (59, 'Automotive and vehicle construction'),
        (74, 'Boiler, container and tank construction'),
        (60, 'Building, agricultural and forestry machinery manufacturing'),
        (65, 'Chemical industry'),
        (81, 'Clean room technology'),
        (61, 'Construction and architectural supplies'),
        (55, 'Drive and gear engineering'),
        (67, 'Electrical industry'),
        (57, 'Fittings engineering'),
        (79, 'Furniture industry'),
        (70, 'Household appliance industry'),
        (71, 'Hydraulic and pneumatic industry'),
        (72, 'Information technology (hardware)'),
        (62, 'Lighting industry'),
        (86, 'Machine tool manufacturing'),
        (77, 'Measurement and control technique, laboratory equipment'),
        (161, 'Mechanical engineering'),
        (76, 'Medical technology'),
        (78, 'Military engineering'),
        (63, 'Mining and tunnel engineering'),
        (64, 'Office machinery and supplies'),
        (85, 'Packaging industry'),
        (80, 'Paper and printing machinery industry'),
        (54, 'Plant engineering and construction'),
        (68, 'Power generation and transmission industry'),
        (69, 'Precision engineering, mechatronics and optics'),
        (66, 'Railway and rail vehicles industry'),
        (82, 'Shipbuilding industry'),
        (83, 'Special purpose machinery manufacturing'),
        (84, 'Telecommunication industry'),
    ]
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=75, blank=False, null=False)
    type_of_business = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    Address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=25, blank=False, null=False)
    country = models.CharField(max_length=25, blank=False, null=False)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    EORI_number = models.CharField(max_length=50, unique=True)
    VAT_number = models.CharField(max_length=50, unique=True)
    industry_Choice = models.IntegerField(choices=INDUSTRY_CHOICES, default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.Name}"


class OutStock(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_out = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Subtract the quantity from the related Stock item
        if self.stock.quantity >= self.quantity:
            self.stock.quantity -= self.quantity
            self.stock.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough stock available")

    def __str__(self):
        return f"OutStock of {self.quantity} {self.stock.name} on {self.date_out}"
