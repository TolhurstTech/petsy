from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import json
import datetime
from .models import Customer, Product, Order, OrderItem, ShippingAddress, Review
from .forms import ReviewForm


# Create your views here.

class ProductList(generic.ListView): 
    '''
    Displays all products from :model:`store.Product` using djangos list view with pagination.

    **Context**

    ``items``
        The items for any open carts to calculate cart totals in the navbar in this view from :model: `OrderItem`

    ``order``
        The users current order/open cart object from :model: `store.Order`

    ``cartItems``
        Total number of cart items for the basket total from :model: `store.Order`

    ``product``
        Sent through by default to display each product

    :template:`store/store.html`
    '''   
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
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']
            context['cartItems'] = cartItems
            
        return context

def cart(request):
    '''
    Fetches or creates a single :model: `store.Order` instance for the current customer dynamically
    by logged in status and sets it's items before rendering it 

    **Context**

    ``items``
        All items with this order ID to be attached to the order from :model: `OrderItem`

    ``order``
        The users current order/open cart object from :model: `store.Order`

    ``cartItems``
        Total number of cart items for the basket total from :model: `store.Order`

    :template:`store/cart.html`
    '''

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Spoof for guest cart
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

    ``product``
        An instance of :model:`store.Product`.

    ``cartItems``
        Total number of cart items for the basket total from :model:`store.OrderItem`

    ``reviews``
        All reviews from :model:`store.Reviews` related to :model:`store.Order`

    ``review_count``
        The count of how many reviews that product has.

    ``review_form``
        The form for creating reviews

    **Template:**

    :template:`store/product_detail.html`
    """

    queryset = Product.objects.filter(draft=1)
    product = get_object_or_404(queryset, slug=slug)

    # Reviews
    reviews = product.product_reviews.all().order_by("-created_on")
    review_count = product.product_reviews.filter(approved=True).count()
    review_form = ReviewForm()

    # Review form logic
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.author = request.user
        review.product = product
        review.save()
        messages.add_message(
            request, messages.SUCCESS,
            'Review submitted and awaiting approval'
        )

    # Create customer and cart
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # spoof for guest
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    return render(
        request,
        "store/product_detail.html",
        {"product": product,
         "cartItems": cartItems,
         "reviews": reviews,
         "review_count": review_count,
         "review_form": review_form,
        },
    )

def checkout(request):
    """
    Display an instance of :model:`store.Order` in the checkout page.

    **Context**

    ``order``
        The customers current open instance of :model:`store.Order`

    ``items``
        All items from :model:`OrderItems` related to thie :model:`store.Order` instance.

    ``cartItems``
        Total number of cart items for the basket total from :model:`store.OrderItem`

    **Template:**

    :template:`store/checkout.html`
    """
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
    """
    Updates the instance of :model:`store.Order` for displaying the cart and checkout pages.
    """

    # Get the body sent in our fetch from updateUserOrder
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
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

    # Delete item if total is zero
    if orderItem.quantity <= 0:
        # Give the user a prompt here to check if they would like to delete it
        orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    ''' 
    Uses json and the fetch api to process the :model:`order` for payment.
    Currently spoofed as out of scope for this assignment.
    '''
    transaction_id = datetime.datetime.now().timestamp()
    data =json.loads(request.body)

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
        # Implement guest cart order processing here
        print('User is not logged in')

    return JsonResponse('Payment Complete', safe=False)

def review_edit(request, slug, review_id):
    ''' 
    View to edit :model:`store.Review` on given :model:`store.Prodct`.
    '''

    if request.method == "POST":

        queryset = Product.objects.filter(draft=1)
        product = get_object_or_404(queryset, slug=slug)
        review = get_object_or_404(Review, pk=review_id)
        review_form = ReviewForm(data=request.POST, instance=review)

        if review_form.is_valid() and review.author == request.user:
            review = review_form.save(commit=False)
            review.product = product
            review.approved = False
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review Updated!')
        else:
            messages.add_messages(request, messages.ERROR, 'Error updating review!')

        return HttpResponseRedirect(reverse('product_detail', args=[slug]))

def review_delete(request, slug, review_id):
    """
    View to delete :model:`store.Review` on given :model:`store.Prodct`.
    """
    queryset = Product.objects.filter(draft=1)
    product = get_object_or_404(queryset, slug=slug)
    review = get_object_or_404(Review, pk=review_id)

    if review.author == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own reviews!')

    return HttpResponseRedirect(reverse('product_detail', args=[slug]))