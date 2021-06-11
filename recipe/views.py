from django.shortcuts import render
from .models import Recipe, Category
from ingredient.models import Ingredient
import os
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CreateRecipeForm, EditRecipeForm
from django.db.models import Q
from django.shortcuts import redirect
from core import settings


def home(request):
    recipes = []
    for category in Category.objects.all():
        recipes += Recipe.objects.filter(category=category)[:3]
    return render(request, 'navigation/index.html', {"recipes": recipes})


def single(request, id):
    recipe = Recipe.objects.get(id=id)
    ingredients = Ingredient.objects.filter(recipe=id)
    return render(request, 'recipe/single.html', {"recipe": recipe, "ingredients": ingredients})


def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/list.html', {"recipes": recipes})


def category(request, id):
    recipes = Recipe.objects.filter(category__id=id).filter(published=True)
    return render(request, 'recipe/list.html', {"recipes": recipes})


def search_results(request):
    query = request.GET.get('q')
    object_list = Recipe.objects.filter(
        Q(title__icontains=query) | Q(category__title__icontains=query) | Q(author__username__icontains=query)
    ).filter(published=True)
    return render(request, 'navigation/search_results.html', {"recipes": object_list})


@staff_member_required
def create_recipe(request):
    if request.method == "POST":
        form = CreateRecipeForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = request.user
            task = form.save()

            return redirect("recipe:edit_recipe", id=task.id)
    else:
        form = CreateRecipeForm()
    return render(request, "recipe/create.html", {"form": form})


@staff_member_required
def edit_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    ingredients = None
    if(request.method == "POST"):
        form = EditRecipeForm(request.POST, request.FILES, instance=recipe)
        if(form.is_valid):
            if not recipe.image.path == os.path.join(settings.MEDIA_ROOT, "default.png"):
                os.remove(recipe.image.path)
            form.save(commit=False)
            form.instance.published = True
            form.save()
            return redirect("recipe:recipe_single", id=id)
    else:
        data = {"title": recipe.title, "image": recipe.image, "description": recipe.description, "price": recipe.price, "category": recipe.category}
        form = EditRecipeForm(initial=data)
    if Ingredient.objects.filter(recipe=id).exists():
        ingredients = Ingredient.objects.filter(recipe=id)
    return render(request, "recipe/edit.html", {"recipe": recipe, "form": form, "ingredients": ingredients})


@staff_member_required
def delete_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('home')