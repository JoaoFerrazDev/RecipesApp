import Services.DBContext as db
from Services.DBContext import _query
import uuid

# In-memory session store
sessions = {}
class User:
    def __init__(self, id, username, email, password, date_of_birth, state):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.state = "public"  #Default state
        self.followers = []
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

    def get_user_info(session_token):
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
            return "Invalid session token"

