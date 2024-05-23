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