import Services.DBContext as db
from Services.DBContext import _query
class User:
    def __init__(self, id, username, email, password, date_of_birth):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.state = "public"  #Default state
        self.followers = []
        self.recipes = []


@staticmethod
def register(username, email, password, date_of_birth):
    if _query(f'SELECT * FROM users WHERE email = {email}'):
        raise ValueError("Email already registered")

        # Insert the new user
    _query(f'INSERT INTO users (username, email, password) VALUES ({username},{email},{password})')

    # Get the last inserted user ID
    user_id = _query('SELECT last_insert_rowid()')[0]

    return User(user_id, username, email, password, date_of_birth)

@staticmethod
def login(email, password):
    db._cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user_data = db._cursor.fetchone()
    if not user_data:
        raise ValueError("Incorrect email or password")

    user_id, username, email, password, date_of_birth, state = user_data
    user = User(user_id, username, email, password, date_of_birth)
    user.state = state
    return user