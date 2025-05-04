from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from .gemini_api import get_gemini_recommendation  # <-- Import

def product_list(request):
    products = Product.objects.all()

    # Create a list of product names
    product_names = [p.name for p in products]

    # Get Gemini recommendation
    recommendation = get_gemini_recommendation(product_names) 

    return render(request, 'store/product_list.html', {
        'products': products,
        'recommendation': recommendation
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})
