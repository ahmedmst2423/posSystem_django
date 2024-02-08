from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Item, Category,Transaction,Customer,Operator,Transaction_Item


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Transaction)
#admin.site.register(Payment)
admin.site.register(Operator)
#admin.site.register(Customer)
admin.site.register(Transaction_Item)
