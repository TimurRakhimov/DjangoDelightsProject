from django import forms
from .models import Ingredient, Purchase, RecipeRequirement, MenuItem

class IngredientForm(forms.ModelForm):
     class Meta:
          model = Ingredient
          fields = ['product_name', 'quantity', 'price']

class PurchaseForm(forms.ModelForm):
     class Meta:
          model = Purchase
          fields = ['menu_item', 'quantity']

class MenuItemForm(forms.ModelForm):
     class Meta:
          model = MenuItem
          fields = ['name', 'price']

class RecipeRequirementForm(forms.ModelForm):
     class Meta:
          model = RecipeRequirement
          fields = ['ingredient', 'quantity_required']