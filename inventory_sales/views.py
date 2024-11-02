from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import MenuItemForm, IngredientForm, PurchaseForm, RecipeRequirementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

def home(request):
    return render(request, 'inventory_sales/home.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'inventory_sales/login.html', {'form': form})
    
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'inventory_sales/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'inventory_sales/ingredient_list.html', {'ingredients': ingredients})

def menu_item_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'inventory_sales/menu_item_list.html', {'menu_items': menu_items})

@login_required
def add_ingredient(request):
     if request.method == 'POST':
          form = IngredientForm(request.POST)
          if form.is_valid():
               ingredient = form.save(commit=False)
               ingredient.user = request.user
               ingredient.save()
               return redirect('ingredient_list')
     else:
          form = IngredientForm()
     return render(request, 'inventory_sales/add-ingredient.html', {'form': form})

@login_required
def add_menu_item(request):
    if request.method == 'POST':
        menu_item_form = MenuItemForm(request.POST)
        if menu_item_form.is_valid():
            menu_item = menu_item_form.save()

            # Get multiple ingredients and quantities from POST data
            ingredients = request.POST.getlist('ingredient')
            quantities = request.POST.getlist('quantity_required')

            # Save associated recipe requirements
            for ingredient_id, quantity in zip(ingredients, quantities):
                if ingredient_id and quantity:
                    ingredient = Ingredient.objects.get(id=ingredient_id)
                    RecipeRequirement.objects.create(
                        menu_item=menu_item,
                        ingredient=ingredient,
                        quantity_required=quantity
                    )

            return redirect('menu_item_list')
    else:
        menu_item_form = MenuItemForm()

    return render(request, 'inventory_sales/add-menu-item.html', {
        'menu_item_form': menu_item_form,
        'ingredients': Ingredient.objects.all(),  # Pass all ingredients to the template
    })

@login_required
def record_purchase(request):
     if request.method == 'POST':
          form = PurchaseForm(request.POST)
          if form.is_valid():
               purchase = form.save(commit=False)
               purchase.user = request.user
               menu_item = purchase.menu_item
               recipe_requirements = menu_item.recipe_requirements.all()

               for recipe_requirement in recipe_requirements:
                    if recipe_requirement.ingredient.quantity < recipe_requirement.quantity_required:
                         return render(request, 'inventory_sales/error.html'), {
                              'message': f"Sorry, we do not have enough {recipe_requirement.ingredient.name} to make {menu_item.name}."
                         }

               for requirement in recipe_requirements:
                    recipe_requirement.ingredient.quantity -= requirement.quantity_required
                    recipe_requirement.ingredient.save()

               purchase.save()
               return redirect('purchase_history')
     else:
          form = PurchaseForm()
     return render(request, 'inventory_sales/record-purchase.html', {'form': form})

@login_required
def purchase_history(request):
    purchases = Purchase.objects.all().order_by('-timestamp')  # Order by most recent first
    return render(request, 'inventory_sales/purchase_history.html', {'purchases': purchases})
