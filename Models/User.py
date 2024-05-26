import Services.DBContext as db
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
        db._cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if db._cursor.fetchone():
            raise ValueError("Email already registered")

        db._cursor.execute('''
                INSERT INTO users (username, email, password, date_of_birth, state)
                VALUES (?, ?, ?, ?, 'public')
            ''', (username, email, password, date_of_birth))

        db._connection.commit()
        user_id = db._cursor.lastrowid

        return User(user_id, username, email, password, date_of_birth)