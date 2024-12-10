import json
from .models import Item

from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import never_cache

@never_cache
@login_required 
def home(request):
    search_query = request.GET.get('search', '') # get search query for search functionality

    price_filter = request.GET.get('price', '') # price filter
    category_filter = request.GET.get('category', '') # type filter

    items = Item.objects.all()

    if search_query:
        items = Item.objects.filter(name__icontains=search_query) # filter name search

    if price_filter == 'asc':
        items = items.order_by('price')  # Low to High
    elif price_filter == 'desc':
        items = items.order_by('-price') # High to Low

    if category_filter:
        items = items.filter(category=category_filter)

    return render(request, 'home.html',{ 'items': items}) # home page

def login_view(request):
    if request.method == 'POST':
        currentUsername = request.POST.get('username')
        currentPassword = request.POST.get('password')

        user = authenticate(request, username=currentUsername, password=currentPassword)

        if user is not None: # if the user is verified
            auth_login(request, user)
            return redirect('home')
        else: # if the user is not verified
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    # if this is a get request just return the login page
    return render(request, 'login.html')

@never_cache
@login_required 
def cart(request):
    items = Item.objects.filter(count__gt=0)
    return render(request, 'cart.html', { 'items': items}) # cart page

def get_cart_count(request):
    cart_items = Item.objects.filter(count__gt=0)
    total_count = sum(item.count for item in cart_items)
    return JsonResponse({'cart_item_count': total_count})

def get_cart_total(request):
    items = Item.objects.filter(count__gt=0)
    total = sum(item.price * item.count for item in items)
    return JsonResponse({'total': total})

def submit(request):
    items = Item.objects.filter(count__gt=0)
    return render(request, 'submit.html', { 'items': items}) # 'Thank you' page

def update_item_count(request, item_id):
    if request.method == "POST":
        try:
            # Get the item from the database
            item = Item.objects.get(id=item_id)

            # Parse the JSON data from the request
            data = json.loads(request.body)
            new_count = data.get('count')

            # Update the count
            item.count = new_count
            item.save()

            return JsonResponse({'success': True})

        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

def reset_count(request, item_id):
    # Ensure the request is a POST request
    if request.method == 'POST':
        try:
            # Fetch the item by ID and reset its count
            item = Item.objects.get(id=item_id)
            item.count = 0  # Reset the count to 0
            item.save()  # Save the updated item to the database
            
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
def reset_all_counts(request):
    if request.method == 'POST':
        # Reset the count of all items to zero
        items = Item.objects.all()
        items.update(count=0)  # Bulk update all items to set count to zero
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')