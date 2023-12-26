import logging
from random import choice
from . import models, forms
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect


logger = logging.getLogger(__name__)


def recipe_info(request, id: int):
    recipe = get_object_or_404(models.Recipe, pk=id)
    context = {
        'recipe': recipe
    }
    return render(request=request, template_name='recipe_book/recipe_info.html', context=context)


def index(request):
    recipes = models.Recipe.objects.filter(
        is_active=True).filter(is_public=True)
    result = []

    if len(recipes) > 5:
        while len(result) < 5:
            tmp = choice(recipes)
            if tmp not in result:
                result.append(tmp)
    else:
        result = recipes
    context = {
        'recipes': result,
    }
    return render(request, 'recipe_book/index.html', context=context)


@login_required
def add_recipe(request):
    form = forms.RecipeForm()

    if request.method == 'POST':
        form = forms.RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            products = form.cleaned_data['products']
            steps = form.cleaned_data['steps']
            make_time = form.cleaned_data['make_time']*60
            is_public = form.cleaned_data['is_public']
            author = User.objects.get(pk=request.user.id)
            recipe = models.Recipe(title=title, description=description, products=products, steps=steps,
                                   make_time=make_time, is_public=is_public, author=author)
            recipe.save()

            if image:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'images')
                fs.save(f"{recipe.id}.{image.name.split(".")[-1]}", image)
                recipe.image = f"images/{recipe.id}.{image.name.split(".")[-1]}"
            recipe.save()
            logger.info(f"Рецепт сохранили by {author}")
            return redirect('home_page')

    context = {
        'form': form,
    }
    return render(request, 'recipe_book/edit.html', context=context)


@login_required
def edit_recipe(request, id: int):
    recipe = get_object_or_404(models.Recipe, pk=id)

    if request.user.id != recipe.author.id:
        return HttpResponse("<h1>Редактирование рецепта может проводить только его автор</h1>")
    
    if request.method == 'POST':
        form = forms.RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            recipe.title = form.cleaned_data['title']
            # recipe.category.set(form.cleaned_data['category'])
            recipe.description = form.cleaned_data['description']
            recipe.products = form.cleaned_data['products']
            recipe.steps = form.cleaned_data['steps']
            recipe.make_time = form.cleaned_data['make_time']*60
            recipe.is_public = form.cleaned_data['is_public']
            recipe.save()
            if image:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'images')
                if recipe.image:
                    fs.delete(str(recipe.image).split('/')[-1])
                fs.save(f"{recipe.id}.{image.name.split(".")[-1]}", image)
                recipe.image = f"images/{recipe.id}.{image.name.split(".")[-1]}"
            recipe.save()
            logger.info(f"Рецепт обновил by {recipe.author}")
            return redirect('home_page')
    form = forms.RecipeForm(instance=recipe)
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe_book/edit.html', context=context)


@login_required
def my_recipes(request):
    recipes = models.Recipe.objects.filter(author_id=request.user.id).filter(is_active=True).order_by('-update_date')
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipe_book/my_recipes.html', context=context)


@login_required
def del_recipe(request, id: int):
    recipe = get_object_or_404(models.Recipe, pk=id)

    if request.user.id != recipe.author.id:
        return HttpResponse("<h1>Удаление рецепта может проводить только его автор</h1>")
    form = forms.DelConfirmForm()
    
    if request.method == 'POST':
        form = forms.DelConfirmForm(request.POST)
        if form.is_valid():
            recipe.is_active = False
            recipe.save()
            logger.info(f"Автор удалил рецепт {recipe.id}")
            return redirect('home_page')
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe_book/del_confirm.html', context=context)

