# app.py
import tornado.ioloop
import tornado.web
from controllers.recipe_controller import RecipeController, RecipeProxy
from views.recipe_view import RecipeView
from models.recipe import Recipe

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Recipe App")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Starting Tornado server on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

    # Initialize MVC components
    view = RecipeView()
    Recipe.add_observer(view)

    controller = RecipeController()
    proxy = RecipeProxy(user={"is_admin": True})  # Simplified user for this example

    # Example usage
    proxy.save_recipe("Pancakes", "Flour, Eggs, Milk", "Mix and cook.")
