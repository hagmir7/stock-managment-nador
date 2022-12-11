from django.db import models
from django.contrib.auth.models import User




class Client(models.Model):
    full_name = models.CharField(max_length=300)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    def paymetn_total(self):
        payments = Payment.objects.filter(client=self)
        return sum([item.montant for  item in payments])
    
    def order_total(self):
        orders = Order.objects.filter(client=self)
        return sum([item.total() for item in orders])
    
    def payment(self):
        return self.order_total() - self.paymetn_total()



class Product(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    colis = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def count(self):
        return self.count()


    



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField(null=True, blank=True)



    def total(self):
        if self.price:
            return self.price * self.quantity
        else:
            return self.product.price * self.quantity
    


class Order(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField(OrderItem, related_name='product_order', blank=True)
    date = models.DateTimeField(auto_now=True)



    def total(self):
        total = [0]
        for item in self.product.all() :
            total.append(item.total())

        return sum(total)


class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    montant = models.FloatField(null=True, blank=True)
    date = models.DateField( null=True, blank=True)
    paid = models.BooleanField(default=False, null=True, blank=True)
    cheque_date = models.DateField(null=True, blank=True)