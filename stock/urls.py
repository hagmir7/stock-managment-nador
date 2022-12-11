from django.urls import path
from .views import *



urlpatterns = [
    path('', index, name='home'),
    path('admins', admins),
    path('client/<int:id>', client),
    path('client/create', createClient),
    path('client/list', listClient),
    path('client/delete/<int:id>', deleteClient),
    path('client/update/<int:id>', updateClient),
    path('client/factur/<int:id>', clientFactur),
    

    path('product/list', listProduct),
    path('product/delete/<int:id>', deleteProduct),
    path('product/update/<int:id>', updateProduct),
    path('product/create', createProduct),
    path('stock/print', stock),



    path('order/list', listOrder),
    path('order/delete/<int:id>', deleteOrder),
    path('order/update/<int:id>', updateOrder),
    path('order/create/<int:id>', createOrder),
    path('order/item/update/<int:id>/<int:order>', updateOrderItem),

    
    path('order-item/create/<int:id>', createOrderItem),
    path('order-item/delete/<int:id>/<int:orderId>', deleteOrderItem),


    path('factur/<int:id>', createFactur),
    

    path('payment/create/<int:id>', createPayment),
    path('payment/list/<int:id>', listPayment),
    path('payment/delete/<int:id>', deletePayment),
    path('all/cheque', allPayments),
    path('current/cheque', curentPayment),
    path('payment/update/<int:id>/<int:client_id>', UpdatePayment),
    path('payment/valid', vilabePayment),
    path('payment/old', oldPayment),
]
