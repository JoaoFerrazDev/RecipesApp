# app.py
import tornado.ioloop
import tornado.web
import Views


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Structure/Index.html", title="Index")

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Register.html", title="Register")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/register", RegisterHandler),
    ], template_path="Views", static_path="static")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Starting Tornado server on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

