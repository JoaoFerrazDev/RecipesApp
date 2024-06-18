from tornado.web import RequestHandler

class Create(RequestHandler):
    def get(self):
        self.render('Recipes/Create.html')

    def post(self):
        try:
            username = self.get_argument('username')
            email = self.get_argument('email')
            password = self.get_argument('password')
            date_of_birth = self.get_argument('birth')
            self.redirect('/login')
        except ValueError as e:
            self.write(str(e))
            self.redirect('/create')