from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product

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
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)