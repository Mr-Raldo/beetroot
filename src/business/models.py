from django.db import models
from akyc.models import Profile, compress
from simple_history.models import HistoricalRecords

class Business(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    entreprenuer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='business')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    wallet_address = models.CharField(max_length=255, null=True, blank=True)
    online_status = models.BooleanField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    neighbourhood = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    portfolio_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    x_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    admin_user_id = models.CharField(max_length=255, null=True, blank=True)
    account_type = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    motto = models.TextField(null=True, blank=True)
    service_type = models.CharField(max_length=255, null=True, blank=True)
    trading_name = models.CharField(max_length=255, null=True, blank=True)
    business_description = models.TextField(null=True, blank=True)
    short_term_goals = models.TextField(null=True, blank=True)
    long_term_goals = models.TextField(null=True, blank=True)
    business_stage = models.CharField(max_length=255, null=True, blank=True)
    business_registration_number = models.CharField(max_length=255, null=True, blank=True)
    target_market_countries = models.CharField(max_length=255, null=True, blank=True)
    target_market_cities = models.CharField(max_length=255, null=True, blank=True)
    short_term_goal = models.TextField(null=True, blank=True)
    long_term_goal = models.TextField(null=True, blank=True)
    trade_sector = models.CharField(max_length=255, null=True, blank=True)
    search_term = models.CharField(max_length=255, null=True, blank=True)
    main_banner_image = models.ImageField(upload_to='images/business/assets/banner', null=True, blank=True)
    logo = models.ImageField(upload_to='images/business/assets/logo', null=True, blank=True)
    is_subscribed = models.BooleanField(null=True, blank=True)
    is_premium_subscribed = models.BooleanField(null=True, blank=True)
    history = HistoricalRecords()
    def save(self, *args, **kwargs):                
        main_banner_image =  compress(self.main_banner_image)                
        logo =  compress(self.logo)                
        self.main_banner_image = main_banner_image               
        self.logo = logo               
        super().save(*args, **kwargs)
    def __str__(self):
        return self.trading_name

class Service(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    entreprenuer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    trade_status = models.CharField(max_length=255, null=True, blank=True)
    is_trending = models.BooleanField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.name}"
    
class ServiceImage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/services_images/', null=True,)
    #calling image compression function before saving the data    
    def save(self, *args, **kwargs):                
        image =  compress(self.image)                
        self.image = image               
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.service.name
    history = HistoricalRecords()

class Product(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    entreprenuer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    trade_status = models.CharField(max_length=255, null=True, blank=True)
    is_trending = models.BooleanField(null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.name}"

class ProductImage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/products_images/', null=True,)
    history = HistoricalRecords()
        #calling image compression function before saving the data    
    def save(self, *args, **kwargs):                
        image =  compress(self.image)                
        self.image = image               
        super().save(*args, **kwargs)
    def __str__(self):
        return self.product.name

    def __str__(self):
        return f"{self.pk} - {self.service}"
