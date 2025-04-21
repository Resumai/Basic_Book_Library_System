import os
import pickle
from ..models.user import User

class UserManager:
    def __init__(self, users_file=r"data\users.pkl"):
        self.users_file = users_file
        self.users : dict[str, User] = self._load_users()
        self.current_user : User  = User()

    def __iter__(self):
        return iter(self.users.values())
    
    def __len__(self):
        return len(self.users)

    def __getitem__(self, index):
        return self.users[index]

    def _get_unused_id(self):
        if self.users == {}:
            return "0000"
        else:
            max_id = 0
            for user in self.users.values():
                if int(user.card_id) > max_id:
                    max_id = int(user.card_id)
            new_id = max_id + 1
            return f"{new_id:04d}"

    
    def save_users(self):
        with open(self.users_file, "wb") as file:
            pickle.dump(self.users, file)


    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "rb") as file:
                return pickle.load(file)
        return {}
    
    # updates the user
    def update_user(self):
        key = self.current_user.login_id
        self.users[key] = self.current_user
        self.save_users()

    # authenticates the user
    def authenticate(self, login_id : str, password):
        user = self.users.get(login_id)
        if user and user.password == password:
            return user
        return False
    
    # adds an admin to the system
    def add_admin(self, username_input, password_input):
        # generates unique id for admin, mb he will need to take some books or smth?
        card_id = self._get_unused_id()
        
        user = User(username_input, password_input, card_id, role = "Admin")
        self.users[username_input] = user
        self.save_users()
        return f"Admin added successfully: Login/Username ID: {username_input}, Password: {password_input}"

    # adds a user to the system
    def add_user(self, username_input, password_input):
        card_id = self._get_unused_id() # generates unique id for user
        user = User(username_input, password_input, card_id, role = "User")
        self.users[card_id] = user
        self.save_users()
        return f"User added successfully: Login/Card ID: {card_id}, Password: {password_input}"

    # removes a user from the system
    def remove_user(self, card_id_input):
        try:
            if self.users[card_id_input].role == "Admin":
                return f"Admin with card ID {card_id_input} cannot be removed."
        except KeyError:
            return f"User with card ID {card_id_input} not found."
        del self.users[card_id_input]
        self.save_users()
        return f"User with card ID {card_id_input} removed successfully."

    # prints all users in the system
    def print_users(self):
        for user in self.users.values():
            if user.role == "Admin":
                print(f"User: {user.username}, Card ID: {user.card_id}, Role: {user.role}")
            else:
                print(f"User: {user.username}, Card ID: {user.card_id}, Role: {user.role}, Password: {user.password}")

    # logs in a user
    def login(self, login_id, password):
        user = self.authenticate(login_id, password)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = User()