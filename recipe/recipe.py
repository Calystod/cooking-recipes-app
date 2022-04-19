from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sys import stderr
from werkzeug.security import generate_password_hash, check_password_hash
# from main import db
#from models import Recipe
from bs4 import BeautifulSoup
from database import helper
from model import recipe
import requests


recipe_bp = Blueprint('recipe', __name__, template_folder='templates')

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@recipe_bp.route('/recipes')
def all_recipes():
    #Recipe.query.all(), 4))
    recipes_json = helper.get_multi('recipes', {})
    print(recipes_json)
    recipes = []
    for recipe_json in recipes_json:
        recipe_object = recipe.Recipe(recipe_json)
        recipes.append(recipe_object)
    print(recipes)
    list_recipes = list(chunks(recipes, 4))
    return render_template('recipe/all_recipes.html', recipes=list_recipes, nb_recipes=len(recipes))

@recipe_bp.route('/recipe')
@login_required
def add_recipe():
    return render_template('recipe/add_recipe.html')

@recipe_bp.route('/recipe', methods=['POST'])
@login_required
def add_recipe_post():
    url = request.form.get('url')
    r = requests.get(url)
    page_source = r.content
    page = BeautifulSoup(page_source, 'html.parser')
    head = page.head
    image = head.find('meta', property="og:image")['content']
    title_recipe = head.find('meta', property="og:title")['content']
    description = head.find('meta', property="og:description")['content'] if head.find('meta', property="og:description") else ''

    new_recipe = {
        'url': url,
        'name': title_recipe,
        'picture': image,
        'description': description
    }
    # add the new user to the database
    helper.add("recipes", new_recipe)

    flash('New recipe add.')
    return redirect(url_for('recipe.add_recipe'))