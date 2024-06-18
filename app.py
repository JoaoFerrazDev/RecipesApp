# app.py
import tornado.ioloop
import tornado.web
import Views
from Controllers import UserController, HomeController, RecipesController
from Services.DBContext import Database


def make_app():
    return tornado.web.Application([
        (r"/", HomeController.Home),
        (r"/register", UserController.Register),
        (r"/login", UserController.Login),
        (r"/create-recipe", RecipesController.Create),
    ], template_path="Views", static_path="static")

if __name__ == "__main__":
    app = make_app()
    app.static_folder = 'static'
    app.listen(5001)
    db = Database()
    print("Starting Tornado server on http://localhost:5001")
    tornado.ioloop.IOLoop.current().start()


