from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) 
    score = models.IntegerField(default=0)
    def __str__(self):
	    return str(self.user)



class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	image = models.ImageField(null=True, blank=True)
	description = models.TextField()
	quantity = models.IntegerField(default=0)

	def __str__(self):
		
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)
	
	@property
	def get_cart_total(self):#total for all items of one order    so we use another som in vieu to sum the total of all orders
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	
	


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address

