from Services.DBContext import _query


class NotificationService:

    @staticmethod
    def notify(followed_id, follower_id):
        username = _query('SELECT username FROM users WHERE id = ?', (follower_id,))
        notification = f"User {username[0][0]} started following you."
        _query('INSERT INTO notifications(notification, user_id) VALUES(?, ?)', (notification, followed_id))

    @staticmethod
    def get_notifications(user_id):
        # Retrieve notifications for a specific user
        user_notifications = _query('SELECT * FROM notifications WHERE user_id = ?', (user_id,))
        return user_notifications
