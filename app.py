# app.py
import tornado.ioloop
import tornado.web
import Views
from Controllers import UserController
from Services.DBContext import Database


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Structure/Index.html", title="Index")

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Auth/Register.html", title="Register")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/register", UserController.RegisterController),
    ], template_path="Views", static_path="static")

if __name__ == "__main__":
    app = make_app()
    app.static_folder = 'static'
    app.listen(8888)
    db = Database()
    print("Starting Tornado server on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()


