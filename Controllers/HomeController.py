from Models.Recipe import Recipe
from Controllers.BaseController import BaseHandler


class Home(BaseHandler):
    def get(self):
        recipes = Recipe.get_recent_recipes()
        self.render('Structure/Index.html', recipes=recipes)
