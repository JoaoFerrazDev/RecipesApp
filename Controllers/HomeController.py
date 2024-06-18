from tornado.web import RequestHandler
from Models.Recipe import Recipe


class HomeController(RequestHandler):
    def get(self):
        recipes = Recipe.get_recent_recipes()
        self.render('Structure/Index.html', recipes=recipes)
