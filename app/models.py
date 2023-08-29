from werkzeug.security import generate_password_hash
from app import db
from datetime import datetime

# Database Initialization
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.users.insert_one(self.__dict__)
        
class Subscriber:
    def __init__(self, email, user_id):
        self.email = email
        self.user_id = user_id
        self.date_added = datetime.utcnow()

    # Methods for saving and querying data
    def save(self):
        db.subscribers.insert_one(self.__dict__)

    @staticmethod
    def find_by_user_id(user_id):
        return db.subscribers.find({"user_id": user_id})
    # ... Other methods ...

