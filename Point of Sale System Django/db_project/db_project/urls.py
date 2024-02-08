"""
URL configuration for db_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pos_app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name = 'home'),
    path('operator-login/',views.operator_login,name = 'operator_login'),
    path('admin-login/',admin.site.urls,name = 'admin_login'),
    path('operator-login/operator-home/operator-dashboard/', views.operator_dashboard, name='operator-dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('operator-logout/', views.operator_logout, name='operator-logout'),
    path('item-delete/',views.item_delete,name = 'item-delete'),
    path('add-items/',views.add_item,name = 'add-item'),
    path('operator-login/operator-home/item-list/',views.display_items_view,name = 'item-list'),
    path('item-list-func/',views.display_items,name = 'item-list-func'),
    path('operator-login/operator-home/operator-dashboard/checkout-page/',views.checkout_view,name = 'checkout-page'),
    path('checkout-process/',views.checkout_process,name = 'checkout-process'),
    path('operator-login/operator-home/operator-dashboard/checkout-page/checkout-process/bill',views.print_bill,name = 'bill'),
    path('operator-login/operator-home/sales/',views.sales,name = 'sales'),
    path('sales-processing/',views.sales_processing,name = 'sales-processing'),
    path('operator-login/operator-home/',views.operator_home,name = 'operator-home'),
   
]



