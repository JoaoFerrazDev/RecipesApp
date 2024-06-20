# app.py
import tornado.ioloop
import tornado.web
import Views
from Controllers import UserController, HomeController, RecipesController, AuthController, AccountController
from Services.DBContext import Database


def make_app():
    return tornado.web.Application([
        (r"/", HomeController.Home),
        (r"/register", UserController.Register),
        (r"/login", UserController.Login),
        (r"/logout", UserController.Logout),
        (r"/profile/(\d+)", UserController.Profile),
        (r"/create-recipe", AuthController.AuthProxyHandler, dict(real_handler_class=RecipesController.Create)),
        (r"/edit-recipe/(\d+)", AuthController.AuthProxyHandler, dict(real_handler_class=RecipesController.Edit)),
        (r"/edit-profile/(\d+)", AuthController.AuthProxyHandler, dict(real_handler_class=UserController.Edit)),
        (r"/my-recipes", AuthController.AuthProxyHandler, dict(real_handler_class=AccountController.Recipes)),
        (r"/my-followers", AuthController.AuthProxyHandler, dict(real_handler_class=AccountController.Followers)),
        (r"/my-subscriptions", AuthController.AuthProxyHandler, dict(real_handler_class=AccountController.Subscriptions)),
        (r"/recipe/(\d+)", RecipesController.RecipePage),
        (r"/follow", AuthController.AuthProxyHandler, dict(real_handler_class=AccountController.Follow)),
        (r"/unfollow", AuthController.AuthProxyHandler, dict(real_handler_class=AccountController.Unfollow)),
        (r"/delete-recipe/(\d+)", AuthController.AuthProxyHandler, dict(real_handler_class=RecipesController.Delete)),
        (r"/notifications", AuthController.AuthProxyHandler, dict(real_handler_class=AccountController.Notifications)),
    ], template_path="Views", static_path="static", cookie_secret="QwErTy123456")


if __name__ == "__main__":
    app = make_app()
    app.listen(8001)
    db = Database()
    print("Starting Tornado server on http://localhost:8001")
    tornado.ioloop.IOLoop.current().start()
