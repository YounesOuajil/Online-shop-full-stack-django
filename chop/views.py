
from rest_framework.authtoken.models import Token  # Import Token from the correct location
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.models import User
from chop.forms.CustomerForm import  CustomerForm
from django.contrib.auth import authenticate,login,logout
from .models import * 
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def USER_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)  # Use Token from the imported location

            if username == 'youne':
                return  redirect('products')
            else:
                products = Product.objects.all()
                return render(request, 'store.html', {'products': products, 'token': token.key})
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login')
    return render(request, 'login.html')






def USER_register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already in use.')

            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email address is already in use.')

            if not form.errors:
                user = User.objects.create_user(username=username, email=email, password=form.cleaned_data['password1'])
                
                # Create a Client instance related to the User
                Customer_instance = Customer(user=user)
                Customer_instance.save()
                print(f"New user created: {user}")
                print(f"Customer created: {Customer_instance}")
                
                return redirect('login')
                
    else:
        form = CustomerForm()

    return render(request, 'register.html', {'form': form})






def homeAdmin(request):
    
    return render(request,'homeAdmin.html')








def logout_view(request):
    logout(request)
    return redirect('login')



def homeUser(request):
    
    return render(request,'homeUser.html')





def checkout(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    items = OrderItem.objects.filter(order__in=orders)
    total_cart_cost = sum(order.get_cart_total for order in orders)
    quantity = sum(item.quantity for item in items)

    context = {
        'orders': orders,
        'total_cart_cost': total_cart_cost,
        'items': items,
        'quantity': quantity
    }

    return render(request, 'checkout.html', context)
   




def store(request):
    products=Product.objects.all()
    return render(request, 'store.html',{'products':products})





def cart(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    items = OrderItem.objects.filter(order__in=orders)
    total_cart_cost = sum(order.get_cart_total for order in orders)
    print(orders)

    #total quntity of items
    quantity=sum(item.quantity for item in items)
    context = {'orders': orders, 'total_cart_cost': total_cart_cost,'items': items,'quantity':quantity}

    return render(request, 'cart.html', context)



@csrf_exempt
def update_cart(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print(f'Received request: product_id={product_id}, action={action}')

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if product.quantity > order_item.quantity:
            order_item.quantity += 1
        else:
            return render(request, 'cart.html', {'error_message': 'This is an error message.'})

    elif action == 'remove':
        if order_item.quantity > 0:
            order_item.quantity -= 1

    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()

    # Calculate the total number of items in the cart
    total_items = sum(item.quantity for item in order.orderitem_set.all())
    
    response_data = {
        'message': 'Item was added',
        'cartItems': total_items,
        'quantity': order_item.quantity,
        'total_cart_cost': order.get_cart_total,
    }
    return JsonResponse(response_data)












def store_search(request):
    query = request.GET.get('q')
    

    if query:
        results = Product.objects.filter(name__icontains=query)  # Perform the actual search based on your model fields
    else:
        results = Product.objects.none()  # Empty queryset if there's no query

    results = {
        'results': results,
        'query': query,
    }

    return render(request, 'store_search.html', results)















def product_detail(request,product_id):

    product = Product.objects.get(pk=product_id)

    return render(request,'product_detail.html',{'product':product})




#vieus of admine



def products(request):
    products = Product.objects.all()
    product_total=Product.objects.count

    order_total=Order.objects.count

    customer_total=Customer.objects.count
    top_5_products = OrderItem.objects.values('product__name').annotate(total_quantity=Count('quantity')).order_by('-total_quantity')[:5]
    print(top_5_products)
    context = {
        'products': products,
        'top_5_products': top_5_products,
        'product_total':product_total,
        'order_total':order_total,
       'customer_total':customer_total,
    }
    return render(request, 'products.html',context )


def up_products(request):
    products = Product.objects.all()

    # Manually construct a list of dictionaries with product data
    product_list = [
        {
            'id': product.id,
            'name': product.name,
            'imageURL': product.imageURL,
            'description': product.description,
            'price': product.price,
            'quantity': product.quantity
            # Add more fields if needed
        }
        for product in products
    ]

    return JsonResponse(product_list, safe=False)



from django.core.files.storage import default_storage

@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('product-name')
        price = request.POST.get('product-price')
        description = request.POST.get('product-description')
        image = request.FILES.get('product-image')
        quantity= request.POST.get('product-quantity')

        product = Product(name=name, price=price, description=description,quantity=quantity)
        product.save()

        if image:  # If an image is uploaded
            product.image = image
            product.save()

        return JsonResponse({'message': 'Product added successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



@csrf_exempt
def update_product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        product.name = request.POST['product-name']
        product.price = request.POST['product-price']
        product.description = request.POST['product-description']
        product.quantity = request.POST['product-quantity']

  

        if 'product-image' in request.FILES:
            image = request.FILES['product-image']
            file_name = f"product_images/{product.id}_{image.name}"
            path = default_storage.save(file_name, image)

            # Update the product's image field with the path
            product.image = path  # Assuming your Product model has an 'image' field

        product.save()
        return JsonResponse({'message': 'Product updated successfully'})

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        # Delete the product with the given product_id
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)
        


from django.db.models import Count
def leaderboard(request):
    customers = Customer.objects.all().order_by('-score')  # Retrieve all customers ordered by score

    context = {
        'customers': customers
    }

    return render(request, 'customer_order.html', context)












def send_order(request):
    if request.method == 'POST' and request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)

        if orders.exists():
            selected_order = orders.latest('date_ordered')
            address = request.POST.get('address')
            city = request.POST.get('city')
            phone = request.POST.get('phone')

            customer = request.user.customer
            request.session['username'] = request.user.username

                        # Increment the score
            customer_id = request.user.customer.id
            customer = Customer.objects.get(id=customer_id)
            customer.score += 1
            customer.save()

            shippingAddress = ShippingAddress.objects.create(
                order=selected_order,
                address=address,
                city=city,
                phone=phone
            )
            shippingAddress.save()
            
            order_items = OrderItem.objects.filter(order=selected_order)
            for order_item in order_items:
                product = order_item.product 
                product.quantity -= order_item.quantity
                product.save()
            
    
    return render(request, 'checkout.html')



from .models import ShippingAddress, Order, OrderItem

def order_list(request):
    order_details = []  # Initialize an empty list to hold order details

    # Fetch all the orders
    orders = Order.objects.all()

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)  # Fetch order items for the order
        shipping_address = ShippingAddress.objects.filter(order=order).first()  # Fetch shipping address for the order

        # Prepare a dictionary with required order details
        order_detail = {
            'order_id': order.id,
            
            'shipping_address': {
                'address': shipping_address.address,
                'city': shipping_address.city,
                'phone': shipping_address.phone,
                'date_added': shipping_address.date_added,
            },
            'order_items': order_items,
        }

        # Append the order detail to the list
        order_details.append(order_detail)

    return render(request, 'order_list.html', {'order_details': order_details})

  















@csrf_exempt
def delete_order(request, order_id):
    
        order = Order.objects.get(id=order_id)
        if order:
            order_items = OrderItem.objects.filter(order=order)
            shipping_address = ShippingAddress.objects.filter(order=order)
            
            if shipping_address.exists():
                shipping_address.delete()
                
            for order_item in order_items:
               order_item.delete()
            
            order.delete()
            return JsonResponse({'message': 'Order and associated items deleted successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Order not found'}, status=404)
 