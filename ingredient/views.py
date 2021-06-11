from django.shortcuts import redirect, render
from recipe.models import Recipe
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from .models import Ingredient
from .forms import IngredientForm


@staff_member_required(login_url="/auth/login/")
def create_ingredient(request, id):
    recipe = Recipe.objects.get(id=id)
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.recipe = Recipe.objects.get(id=id)
            form.save()
            return redirect("recipe:edit_recipe", id=recipe.id)
    else:
        form = IngredientForm()
    return render(request, "recipe/ingredient/create.html", {"recipe": recipe, "form": form})


@staff_member_required(login_url="/login/")
def delete_ingredient(request, id):
    ingredient = Ingredient.objects.get(id=id)
    ingredient.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
