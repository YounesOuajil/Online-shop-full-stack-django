from .models import *


from django.contrib.auth import get_user_model

def user_info(request):
    customer = None
    if request.user.is_authenticated:
        User = get_user_model()  # Get the User model dynamically
        try:
            customer = User.objects.get(id=request.user.id).customer
            orders = Order.objects.filter(customer=customer)
            items = OrderItem.objects.filter(order__in=orders)
            cartItemsPN = sum(item.quantity for item in items)
            return {'cartItemsPN': cartItemsPN}
        except User.customer.RelatedObjectDoesNotExist:
            # User doesn't have a related customer object, handle this as you wish
            pass

    return {'customer': customer}
