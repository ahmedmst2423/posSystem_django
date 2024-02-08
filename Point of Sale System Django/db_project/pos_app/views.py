from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
from django.db import connection
from django.http import HttpResponse
import json
from django.utils import timezone
import datetime
import time
import zoneinfo
def home(request):
    return render(request, 'home.html')

@csrf_protect

def operator_login(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(user.pk)
            login(request, user)
            first_name = request.user.first_name
            last_name = request.user.last_name
            name = first_name + " " + last_name
            return redirect('operator-home')
        else:
            pass

   
    return render(request, 'operator_login.html')

@csrf_protect

def operator_dashboard(request):
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    name = first_name + " " + last_name
    #return redirect('operator-home')
    return render(request, 'operator_dashboard.html', {'username': name})


@csrf_protect
@login_required
def add_item(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id') 
        print(f"item_id Received", item_id)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT pos_app_item.item_id AS item_id, pos_app_item.name AS item_name, 
                           pos_app_item.price AS price, pos_app_category.name AS category_name,pos_app_item.stock AS stock
                    FROM pos_app_item
                    INNER JOIN pos_app_category ON pos_app_category.category_id = pos_app_item.category_id_id
                    WHERE pos_app_item.item_id = %s
                """, [item_id])

                row = cursor.fetchone()

            if row:
                item_data = {
                    'item_id': row[0],
                    'item_name': row[1],
                    'price': row[2],
                    'category_name': row[3],
                    'stock': row[4],
                }

                message = f'Item with ID {item_id} found.'
                
                response_data = {'status': 'success', 'message': message, 'item_data': item_data}
                print(response_data)
                #return render(request, 'operator_dashboard.html', response_data, status=200)
                return JsonResponse(response_data,status = 200)
            else:
                message = f'Item with ID {item_id} not found.'
                print(message)
                response_data = {'status': 'error', 'message': message}
                #return render(request, 'operator_dashboard.html', response_data, status=404)
                return JsonResponse(response_data,status = 404)
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            response_data = {'status': 'error', 'message': error_message}
            #return render(request, 'operator_dashboard.html', response_data, status=500)
            return JsonResponse(response_data,status = 500)

    # Handle other HTTP methods if needed
    return render(request, 'operator_dashboard.html', {'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required(login_url='operator-login') 
def operator_logout(request):
    logout(request)
    return redirect('operator_login')




@login_required(login_url='operator-login')
@csrf_protect
def item_delete(request):
    item_id = request.GET.get('item_id')
    print(item_id)
    with connection.cursor() as cursor:
        cursor.execute("""
           SELECT pos_app_item.item_id AS item_id, pos_app_item.name AS item_name, 
                           pos_app_item.price AS price, pos_app_category.name AS category_name
                    FROM pos_app_item
                    INNER JOIN pos_app_category ON pos_app_category.category_id = pos_app_item.category_id_id
                    WHERE pos_app_item.item_id = %s
        """, [item_id])
        row = cursor.fetchone()

    if row:
        # Item found, delete it (add your deletion logic here)
        # ...

        # Respond with a success message
        response_data = {'status': 'success', 'message': 'Item deleted successfully'}
        return JsonResponse(response_data, status=200)
    else:
        # Item not found
        response_data = {'status': 'error', 'message': 'Item not found'}
        return JsonResponse(response_data, status=404)


@csrf_protect
@login_required(login_url='operator-login') 
def display_items_view(request):
    return render(request,'item_list.html')
def display_items(request):
    sort_parameter = request.GET.get('sort', None)
    order = request.GET.get('order', None)

    query = """
           SELECT pos_app_item.item_id AS item_id, pos_app_item.name AS name, 
                    pos_app_item.price AS price,pos_app_item.stock AS stock,pos_app_category.name AS category
                    FROM pos_app_item
                    INNER JOIN pos_app_category ON pos_app_category.category_id = pos_app_item.category_id_id
        """

    if sort_parameter and sort_parameter != "none" and order:
        query += f" ORDER BY {sort_parameter} {'ASC' if order == 'asc' else 'DESC'}"

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        raw_rows = cursor.fetchall()

        print("Raw Row Data:", raw_rows)

        items = [dict(zip(columns, row)) for row in raw_rows]

    return JsonResponse(items, safe=False)





def checkout_view(request):
    return render(request,'checkout_page.html')



@login_required(login_url='operator-login')
@csrf_protect   
def checkout_process(request):
     if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))

       
        grand_total = data.get('grandTotal')
        item_ids = data.get('itemIds')
        quantities = data.get('quantities')
        operator_id  = request.user.operator_id
        current_date = data.get('date')
        current_time = data.get('time')
        payType = data.get('payType')
        

        
        
        print('Grand Total:', grand_total)
        print('Item IDs:', item_ids)
        print('Quantities:', quantities)
        print('Operator ID: ', operator_id)
        with connection.cursor() as cursor:
         cursor.execute("""
        INSERT INTO pos_app_transaction (amount, operator_id_id,customer_id_id, payment_type,time,date)
        VALUES (%s, %s, %s, %s,%s,%s);
    """, [grand_total, operator_id,None,payType,current_time,current_date])
         
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(transaction_id) FROM pos_app_transaction")
            transaction_id = cursor.fetchone()[0]
        for i in range(0,len(item_ids)):

            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO pos_app_transaction_item (transaction_id_id, item_id_id, qty)
                VALUES (%s, %s,%s);
            """, [transaction_id, item_ids[i],quantities[i]])
                
        with connection.cursor() as cursor:
            for item_id, quantity in zip(item_ids, quantities):
                query = f"""
                    UPDATE pos_app_item
                    SET stock = stock - {quantity}
                    WHERE item_id = {item_id};
                """
                cursor.execute(query)
                

        


       

        return JsonResponse({'status': 'success'})

def print_bill(request):
    return render(request,'bill.html')


@csrf_protect
@login_required(login_url='operator-login') 
def sales(request):
    return render(request,'sales.html')
@csrf_protect
@login_required(login_url='operator-login') 
def sales_processing(request):
    with connection.cursor() as cursor:
        cursor.execute('''
      WITH ItemSales AS (
    SELECT
        i.category_id_id,
        ti.qty,
        t.amount,
        t.transaction_id
    FROM
        pos_app_item i
    LEFT JOIN
        pos_app_transaction_item ti ON i.item_id = ti.item_id_id
    LEFT JOIN
        pos_app_transaction t ON ti.transaction_id_id = t.transaction_id
)

SELECT
    c.name AS category_name,
    COALESCE(SUM(ItemSales.qty), 0) AS total_items_sold,
    COALESCE(SUM(ItemSales.amount), 0) AS total_amount,
    COUNT(DISTINCT ItemSales.transaction_id) AS transaction_count
FROM
    pos_app_category c
RIGHT JOIN
    ItemSales ON c.category_id = ItemSales.category_id_id
GROUP BY
    c.category_id
ORDER BY
    c.category_id;

        ''')
        result = cursor.fetchall()

    
    sales_data = [
        {'category_name': row[0], 'total_sales': row[1], 'total_amount': row[2]}
        for row in result
    ]
    print(sales_data)
    # Render the sales.html template with the sales data as JSON
    return JsonResponse({'sales_data': sales_data})
@csrf_protect
@login_required(login_url='operator-login')          
def operator_home(request):
    return render(request,'operator_home.html')



"""

def check_customer(request):
    
    customer_id = request.POST.get('customer_id')
    print("Customer_Id: ",customer_id)
    customer_id = 5671
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM pos_app_customer WHERE customer_id = %s ",[customer_id])
        result = cursor.fetchone()[0]
    print(result)
    if result:
        return JsonResponse({'status':'success'},status = 200)
    else:
        return JsonResponse({'status':'failure'},status = 400)



"""

    
        
        
    

