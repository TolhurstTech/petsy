from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import json
import datetime
from .models import Customer, Product, Order, OrderItem, ShippingAddress


# Create your views here.

class ProductList(generic.ListView):    
    model = Product
    queryset = Product.objects.filter(draft=1)
    template_name = "store/store.html"
    paginate_by = 6

    # Override class context method to pass cart total as cartItems to the view template
    def get_context_data(self,**kwargs):
        # Check if guest cart
        if self.request.user.is_authenticated:
            # Get customer or create it if a new user
            try:
                customer = customer = self.request.user.customer
            except AttributeError:
                customer, created = Customer.objects.get_or_create(user=self.request.user, name=self.request.user.first_name + " " + self.request.user.last_name, email=self.request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            context = super(ProductList,self).get_context_data(**kwargs)
            context['cartItems'] = order.get_cart_items
        else:
            context = super(ProductList,self).get_context_data(**kwargs)
            context['cartItems'] = ['get_cart_items']
        return context

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

    # Quick way to send cart total to the template for the navbar
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {
        'items' : items,
        'order' : order,
        'cartItems': cartItems
    }
    return render(request, 'store/cart.html', context)

def product_detail(request, slug):
    """
    Display an individual :model:`store.Product`.

    **Context**

    ``post``
        An instance of :model:`store.Product`.

    **Template:**

    :template:`store/product_detail.html`
    """

    queryset = Product.objects.filter(draft=1)
    product = get_object_or_404(queryset, slug=slug)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    return render(
        request,
        "store/product_detail.html",
        {"product": product,
         "cartItems": cartItems
        },
    )

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {
        'items' : items,
        'order' : order,
        'cartItems': cartItems
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
    # Get or create the item
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Update item quantity
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    # Save the item
    orderItem.save()

    # Delete  item if total is zero
    if orderItem.quantity <= 0:
        # Give the user a prompt here to check if they would like to delete it
        orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data =json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        # Check cart items haven't been manipulated in front end with JS before setting order to complete
        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['county'],
            postcode=data['shipping']['postcode'],
        )

    else:
        print('User is not logged in')

    return JsonResponse('Payment Complete', safe=False)