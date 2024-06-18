from tornado.web import RequestHandler

from Models.User import User

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
