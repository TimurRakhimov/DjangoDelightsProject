from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
     product_name = models.CharField(max_length=30)
     quantity = models.IntegerField()
     price = models.IntegerField()
     user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
          return self.product_name

class MenuItem(models.Model):
     price = models.IntegerField()
     name = models.CharField(max_length=30)

     def __str__(self):
          return self.name


class RecipeRequirement(models.Model):
     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='recipe_requirements')
     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
     quantity_required = models.FloatField()

     def __str__(self):
          return f"{self.quantity_required} of {self.ingredient.name} for {self.menu_item.name}"

class Purchase(models.Model):
     quantity = models.IntegerField()
     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
     timestamp = models.DateTimeField(auto_now_add=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
          return f" Purchase {self.quantity} of {self.menu_item.name} on {self.timestamp}"