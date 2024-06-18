# app.py
import tornado.ioloop
import tornado.web
import Views
from Controllers import UserController, HomeController, RecipesController, AuthController
from Services.DBContext import Database


def make_app():
    return tornado.web.Application([
        (r"/", HomeController.Home),
        (r"/register", UserController.Register),
        (r"/login", UserController.Login),
        (r"/create-recipe", AuthController.AuthProxyHandler, dict(real_handler_class=RecipesController.Create)),
    ], template_path="Views", static_path="static", cookie_secret="QwErTy123456")


if __name__ == "__main__":
    app = make_app()
    app.static_folder = 'static'
    app.listen(5001)
    db = Database()
    print("Starting Tornado server on http://localhost:5001")
    tornado.ioloop.IOLoop.current().start()


