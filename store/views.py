from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Product, Order

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
    return JsonResponse('Item was added', safe=False)