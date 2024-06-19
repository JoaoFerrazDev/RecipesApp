from tornado.web import RequestHandler

from Models.User import User

class Recipes(RequestHandler):
    def get(self):
        session_token = self.get_secure_cookie("session_token")

        if session_token:
            session_token = session_token.decode('utf-8')
            user_info = User.get_user_info(session_token)
            recipes = User.get_user_recipes(user_info.id)
            self.render('Recipes/Index.html', recipes=recipes)

class Notifications(RequestHandler):
    def get(self):
        notifications = User.get_user_info().notifications.all()
        self.render('Account/Notifications.html', notifications=notifications)


class Followers(RequestHandler):
    def get(self):
        followers = User.get_user_info().followers.all()
        self.render('Account/Followers.html', followers=followers)


class Subscriptions(RequestHandler):
    def get(self):
        subscriptions = User.get_user_info().subscriptions.all()
        self.render('Account/Subscriptions.html', subscriptions=subscriptions)
