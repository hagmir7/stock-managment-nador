from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import timedelta, date, datetime


@login_required(login_url='/accounts/login')
def index(request):
    today = date.today()
    seven_day_before = today + timedelta(days=5) 
    list = Payment.objects.filter(cheque_date__lt=seven_day_before, cheque_date__gte=today).filter(type="Cheque").order_by('cheque_date')
    paginator = Paginator(list, 50) 
    page_number = request.GET.get('page')
    payments = paginator.get_page(page_number)
    context = {
        'users': User.objects.all,
        'clients': Client.objects.all,
        'orders' : Order.objects.all,
        'products' : Product.objects.all,
        'payments': payments,
        'title': 'Stock Management'
    }
    return render(request, 'index4.html', context)









def admins(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title' : "Liste des admins"
    }
    return render(request, 'admins.html', context)


def createClient(request):
    form = ClientForm()
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/client/list')

    context = {
        'from': form,
        'title' : 'Créer un nouveau client'
    }
    return render(request, 'client/create.html', context)

def updateClient(request, id):
    client = Client.objects.get(id=id)
    form = ClientForm(instance=client)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully')
            return redirect('/client/list')

    context = {
        'from': form,
        'client' : client,
        'title' : 'Créer un nouveau client'
    }
    return render(request, 'client/update.html', context)


def listClient(request):
    
    if request.method == 'POST':
        query = request.POST.get('search')
        full_name = Client.objects.filter(full_name__icontains=query)
        # id = Client.objects.filter(id=query)
        email = Client.objects.filter(email__icontains=query)
        clients = full_name | email
    else:
        query = ''
        list = Client.objects.all()
        paginator = Paginator(list, 50)
        page_number = request.GET.get('page')
        clients = paginator.get_page(page_number)
    context = {'clients': clients, 'query': query, 'title': 'Leste de clients'}
    return render(request, 'client/list.html', context)


def deleteClient(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    messages.success(request, 'Client supprimé avec succès...')
    return redirect('/client/list')




# Command

def createProduct(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/product/list')

    context = {
        'from': form,
        'title' : 'Créer un nouveau Product'
    }
    return render(request, 'product/create.html', context)

def updateProduct(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('/product/list')

    context = {
        'product' : product,
        'title' : 'Éditer un Product'
    }
    return render(request, 'product/update.html', context)


def listProduct(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        full_name = Product.objects.filter(name__icontains=query).order_by('-stock')
        code = Product.objects.filter(code__icontains=query).order_by('-stock')
        products = full_name | code
    else:
        query = ''
        list = Product.objects.all().order_by('date').order_by('-stock')
        paginator = Paginator(list, 50)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
    context = {'products': products, 'title': 'Liste des porduits', 'query': query}
    return render(request, 'product/list.html', context)


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product supprimé avec succès...')
    return redirect('/product/list')


def stock(request):
    products = Product.objects.all().order_by('-stock')
    context = {
        'products': products,
        'title': 'Liste de Stock'
    }
    return render(request, 'product/stock.html', context)

# Oreder


def createOrder(request, id):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/order/list')
    else:
        order = Order.objects.create(admin=request.user, client=Client.objects.get(id=id))
        return redirect(f"/order/update/{order.id}")
    context = {
        'form': form,
        'clients' : Client.objects.all(),
        'products': Product.objects.all(),
        'title' : 'Créer un nouveau Order'
    }
    return render(request, 'order/create.html', context)

def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Order updated successfully')
            return redirect('/order/list')

    context = {
        'form': form,
        'order' : order,
        'clients' : Client.objects.all(),
        'products': Product.objects.all(),
        'title' : 'Éditer un order'
    }
    return render(request, 'order/update.html', context)


def listOrder(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        full_name = Order.objects.filter(client__full_name__icontains=query)
        orders = full_name 
    else:
        query = ''
        list = Order.objects.all()
        paginator = Paginator(list, 50)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)
    context = {'orders': orders, 'query': query, 'title': 'List des facture'}
    return render(request, 'order/list.html', context)


def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    for item in order.product.all():
        item.product.stock = item.product.stock + item.quantity
        item.product.save()
    order.delete()
    messages.success(request, 'Order supprimé avec succès...')
    return redirect('/order/list')




def createOrderItem(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)

        product = Product.objects.get(id=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        if product.stock < int(quantity):
            messages.warning(request, "Stok n'est pas disponible.", 'danger')
            return redirect(f"/order/update/{order.id}")
        else:
            if form.is_valid():
                item = form.save()
                product.stock = product.stock - int(quantity)
                product.save()
                order.product.add(item)
    return redirect(f"/order/update/{order.id}")

def updateOrderItem(request, id, order):
    item = OrderItem.objects.get(id=id)
    form = OrderItemForm(instance=item)
    if request.method == "POST":
        form = OrderItemForm(request.POST, instance=item)
        new_product = request.POST.get('product')
        new_quantity = request.POST.get('quantity')

        product = Product.objects.get(id=new_product)
        if int(new_quantity) < int(item.quantity):
            product.stock = product.stock +  (int(item.quantity) - int(new_quantity))
            product.save()
            if form.is_valid():
                form.save()
                messages.success(request, "Le produit a été modifié avec succès...")
                return redirect(f'/order/update/{order}')
        elif int(new_quantity) > int(item.quantity) :
            product.stock = product.stock -  (int(new_quantity) - int(item.quantity))
            product.save()
            if form.is_valid():
                form.save()
                messages.success(request, "Le produit a été modifié avec succès...")
                return redirect(f'/order/update/{order}')
        elif int(new_quantity) > product.stock:
            messages.error(request, "Stok n'est pas disponible.", 'danger')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, "Le produit a été modifié avec succès...")
                return redirect(f'/order/update/{order}')
                

    context = {
        'item': item,
        'products' : Product.objects.all(),
        'title' : 'Modifier la facture du produit'
        
    }

    return render(request, 'order/update-order-item.html', context)



def deleteOrderItem(request, id, orderId):
    orderItem = OrderItem.objects.get(id=id)
    orderItem.product.stock = orderItem.product.stock + orderItem.quantity
    orderItem.product.save()
    orderItem.delete()
    messages.success(request, 'Product supprimé avec succès...')
    return redirect(f'/order/update/{orderId}')





def createFactur(request, id):
    order = get_object_or_404(Order, id=id)
    context = {
        'order' : order,
        'clients' : Client.objects.all(),
        'products': Product.objects.all(),
        'title' : f'Client : Mr. {order.client}'
    }
    return render(request, 'order/factur.html', context)



def client(request, id):
    client = get_object_or_404(Client, id=id)
    orders = Order.objects.filter(client=client).order_by('-date')
    context = {
        'client': client,
        'orders': orders,
        "title": 'Liste de facture'
        
    }
    return render(request, 'client/client.html', context)

def clientFactur(request, id):
    client = get_object_or_404(Client, id=id)
    orders = Order.objects.filter(client=client).order_by('-date')
    context = {
        'client': client,
        'orders': orders
    }
    return render(request, 'client/client.html', context)




def client(request, id):
    client = get_object_or_404(Client, id=id)
    orders = Order.objects.filter(client=client).exclude(product__isnull=True).order_by('-date')
    payments = Payment.objects.filter(client=client)
    context = {
        'client': client,
        'orders': orders,
        'payments' : payments,
         "title": 'Liste de facture'
    }
    return render(request, 'client/client-page.html', context)



def createPayment(request, id):
    form = PaymentForm()
    client =  Client.objects.get(id=id)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            messages.success(request, 'Paiement créé avec succès...')
            return redirect(f"/payment/list/{client.id}")
       
    context = {
        'form': form,
        'client': client,
        "title": "Nouveau facture"
    }
    return render(request, 'payment/create.html', context)

def listPayment(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        query = request.POST.get('search')
        payments = Payment.objects.filter(client=client).order_by('-date').filter(client__full_name__icontains=query)
        pass
    else:
        query = ''
        list = Payment.objects.filter(client=client).order_by('-date')
        paginator = Paginator(list, 40)
        page_number = request.GET.get('page')
        payments = paginator.get_page(page_number)
    
    context = {
        'client': client,
        'payments' : payments,
        'title': f"Payment de Mr {client}",
        'query' : query
    }
    return render(request, 'payment/list.html', context)



def allPayments(request):
    if request.method == "POST":
        query = request.POST.get('search') 
        payments = Payment.objects.filter(type="Cheque").filter(client__full_name__icontains=query).order_by('-date')
    else:
        query = ''
        list = Payment.objects.filter(type="Cheque").order_by('-date')
        paginator = Paginator(list, 50) 
        page_number = request.GET.get('page')
        payments = paginator.get_page(page_number)

    context = {
        'payments' : payments,
        'title': f"List des Cheques",
        'query': query
    }
    return render(request, 'payment/all.html', context)


from datetime import timedelta, date

def curentPayment(request):
    today = date.today()
    seven_day_before = today + timedelta(days=5) 

    if request.method == "POST":
        query = request.POST.get('search') 
        payments = Payment.objects.filter(cheque_date__lt=seven_day_before, cheque_date__gte=today).filter(type="Cheque", client__full_name__icontains=query).order_by('cheque_date')
    else:
        
        query = ''
        list = Payment.objects.filter(cheque_date__lt=seven_day_before, cheque_date__gte=today).filter(type="Cheque").order_by('cheque_date')
        paginator = Paginator(list, 50) 
        page_number = request.GET.get('page')
        payments = paginator.get_page(page_number)

    context = {
        'payments' : payments,
        'title': f"List des Cheques",
        'query': query
    }
    return render(request, 'payment/current.html', context)





def deletePayment(request, id):
    payment = Payment.objects.get(id=id)
    payment.delete()
    messages.success(request, 'Paiement supprimé avec succès')
    return redirect(f'/all/cheque')





def UpdatePayment(request, id, client_id):
    payment = Payment.objects.get(id=id)
    client = Client.objects.get(id=client_id)
    form = PaymentForm(instance=payment)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            messages.success(request, 'Paiement modifié avec succès...')
            return redirect(f'/payment/list/{client.id}')
       
    context = {
        'form': form,
        'payment': payment,
        "title": "Modifier le paiement"
    }
    return render(request, 'payment/update.html', context)

def vilabePayment(request):
    if request.method == "POST":
        query = request.POST.get('search') 
        payments = Payment.objects.filter(paid=False, client__full_name__icontains=query).order_by('cheque_date')
    else:
        query = ''
        list = Payment.objects.filter(paid=False).order_by('cheque_date')
        paginator = Paginator(list, 50) 
        page_number = request.GET.get('page')
        payments = paginator.get_page(page_number)

    context = {
        'payments': payments,
        'title': 'Chèques non tirés',
         'query': query
    }
    return render(request, 'payment/valid.html', context)


def oldPayment(request):
    if request.method == "POST":
        query = request.POST.get('search') 
        payments = Payment.objects.filter(paid=True, client__full_name__icontains=query).order_by('cheque_date')
    else:
        query = ''
        list = Payment.objects.filter(paid=True).order_by('cheque_date')
        paginator = Paginator(list, 50) 
        page_number = request.GET.get('page')
        payments = paginator.get_page(page_number)

    context = {
        'payments': payments,
        'title': 'Chèques expirés',
         'query': query
    }
    return render(request, 'payment/valid.html', context)