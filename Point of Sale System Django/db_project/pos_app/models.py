# models.py file in your app
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group, Permission
from django.core.validators import MinValueValidator

class Item(models.Model):

    item_id = models.AutoField(primary_key=True)
    
    
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
  
    name = models.CharField(max_length=255)
 
    stock = models.IntegerField(validators=[MinValueValidator(limit_value=0), ])
 
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(limit_value=0)])

    def __str__(self):
        return f"{self.item_id}  - {self.name} - {self.category_id}"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
       return f"{self.name}  - {self.category_id}"

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    customer_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.customer_id}"

class OperatorManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        operator_id = extra_fields.pop('operator_id', None)  # Retrieve operator_id from extra_fields

        user = self.create_user(username, password=password, **extra_fields)

        if operator_id is not None:
            user.operator_id = operator_id
            user.save(using=self._db)

        return user

class Operator(AbstractBaseUser, PermissionsMixin):
    operator_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, default='default_username')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    hire_date = models.DateField(null=True)
    is_working = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = OperatorManager()
    last_login = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'username'
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.operator_id}"
    
    groups = models.ManyToManyField(Group, blank=True, related_name='operator_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='operator_user_permissions')
    
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    operator_id = models.ForeignKey('Operator', on_delete=models.SET_NULL, null = True)
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    customer_id = models.ForeignKey('Customer', null=True, blank=True, on_delete=models.SET_NULL)
    payment_type_choices = [
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
    ]
    payment_type = models.CharField(max_length=20, choices=payment_type_choices,null = True)
    def __str__(self):
        return f"Transaction ID: {self.transaction_id} - Amount: {self.amount}"
    
class Transaction_Item(models.Model):
    transaction_id = models.ForeignKey('Transaction',null = True, blank = False, on_delete = models.SET_NULL)
    item_id = models.ForeignKey('Item', null = True,blank = False,on_delete= models.SET_NULL)
    qty = models.IntegerField(default = 1)
    def __str__(self):
        return f"Transaction ID: {self.transaction_id} - Item_ID: {self.item_id}"
    
'''
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
   
    payment_type = models.CharField(max_length=20, choices=payment_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment ID: {self.payment_id} - Payment Type: {self.payment_type} - Amount: {self.amount}"
'''
