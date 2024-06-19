import Services.DBContext as db
from Services.DBContext import _query
import uuid

# In-memory session store
sessions = {}


class User:
    def __init__(self, id, username, email, password, date_of_birth, state="public", num_of_following=0, num_of_followers=0):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.state = state
        self.followers = []
        self.numOfFollowers = num_of_followers
        self.numOfFollowing = num_of_following
        self.subscriptions = []
        self.recipes = [],
        self.notifications = []


    @staticmethod
    def register(username, email, password, date_of_birth):
        # Check if email is already registered
        if _query('SELECT * FROM users WHERE email = ?', (email,)):
            raise ValueError("Email already registered")

        # Insert the new user
        _query('INSERT INTO users (username, email, password, date_of_birth) VALUES (?, ?, ?, ?)',
               (username, email, password, date_of_birth))

        # Get the last inserted user ID
        user_id = _query('SELECT last_insert_rowid()')[0][0]

        return User(user_id, username, email, password, date_of_birth)

    @staticmethod
    def login(email, password):
        user_data = _query('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        if not user_data:
            return None

        user = User(*user_data[0])
        session_token = User.create_session(user)
        return session_token

    @staticmethod
    def create_session(user):
        session_token = str(uuid.uuid4())
        sessions[session_token] = user
        return session_token

    @staticmethod
    def get_user_from_session(session_token):
        return sessions.get(session_token)

    @staticmethod
    def logout(session_token):
        if session_token in sessions:
            del sessions[session_token]

    def get_user_info(session_token:str):
        user = User.get_user_from_session(session_token)
        if user:
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_of_birth': user.date_of_birth,
                'state': user.state,
                'followers': user.followers,
                'recipes': user.recipes,
                'notifications': user.notifications,
                'subscriptions': user.subscriptions
            }
        else:
            return None

    def get_user_recipes(user_id):
        recipes = _query('SELECT * FROM recipes WHERE user_id = ?', (user_id,))
        return recipes

    def get_user_profile(id):
        user_data = _query('SELECT u.*, COUNT(f.follower) AS numFollowing, (SELECT COUNT(*) FROM followers WHERE following = u.id) As numFollowers FROM users u LEFT JOIN followers f ON f.follower = u.id WHERE u.id == ? GROUP BY u.id;', (id))
        user_info = User(*user_data[0])
        return user_info

    @staticmethod
    def follow_user(current_user_id, followed_user_id):
        query = 'INSERT INTO followers (follower,following) VALUES (?,?)'
        return _query(query, (current_user_id, followed_user_id))
