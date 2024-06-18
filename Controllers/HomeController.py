from tornado.web import RequestHandler
from Models.Recipe import Recipe


class Home(RequestHandler):
    def get(self):
        recipes = Recipe.get_recent_recipes()
        self.render('Structure/Index.html', recipes=recipes)
