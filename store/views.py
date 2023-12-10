from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import json
from .models import Product, Order, OrderItem


# Create your views here.

class ProductList(generic.ListView):
    model = Product
    queryset = Product.objects.filter(draft=1)
    template_name = "store/store.html"
    paginate_by = 6

def store(request):
    context = {}
    return render(request, 'store/store.html', context)

def cart(request):
    '''
    Fetches or creates a single :model: `Order` instance for the current customer dynamically
    by logged in status and sets it's items before rendering it 

    **Context**

    ``items``
        All items with this order ID to be attached to the order

    ``order``
        The users current order/open cart object

    :template:`store/cart.html`
    '''
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {
        'items' : items,
        'order' : order
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {
        'items' : items,
        'order' : order
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    # Get the body sent in our fetch from updateUserOrder
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)
    
    # Get the customer
    customer = request.user.customer
    # Get the product
    product = Product.objects.get(id=productId)
    # Get or create the order
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # Get of create the item
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Update item quantity
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    # Delete  item if total is zero
    if orderItem.quantity <= 0:
        orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)