from uuid import uuid4
from ..database.Collection import UserDataCollection
from ..database.data_objects import User

from typing import Optional
from dataclasses import dataclass


class UserAuthenticationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AuthenticationService:
    def __init__(self, db_connector):
        db = db_connector.connect()
        self.user_collection = db.get_collection("user_data")

    def _generate_user_id(self) -> str:
        user_id = str(uuid4())
        # Collision is unlikely but let's handle it anyway
        while self.get_user_by_id(user_id) is not None:
            user_id = str(uuid4())
        return user_id

    @staticmethod
    def _validate_signup_request_data(request) -> Optional[dict]:
        try:
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]
            return {
                "email": email,
                "username": username,
                "password": password,
                "role": role,
            }
        except:
            return None

    @staticmethod
    def _validate_signin_request_data(request) -> Optional[dict]:
        try:
            email = request.form["email"]
            password = request.form["password"]
            return {"email": email, "password": password}
        except:
            return None

    @classmethod
    def validate_request_data(cls, request, signup: bool = True):
        """
        Validate the flask request data
        :param signup: if True the function will check for sign up data, if false it will check for sign in data
        """
        request_data = None
        if signup:
            request_data = cls._validate_signup_request_data(request)
        else:
            request_data = cls._validate_signin_request_data(request)
        if not request_data:
            raise UserAuthenticationException("Form data is not valid!")
        return request_data

    def get_user_by_email(self, email: str = "") -> Optional[User]:
        """
        Try getting a user from the database, returns None if not found.
        """
        if email != "":
            return self.user_collection.retrieve_by_email(email)
        return None

    def get_user_by_id(self, id: str = "") -> Optional[User]:
        """
        Try getting a user from the database, returns None if not found.
        """
        if id != "":
            return self.user_collection.retrieve_by_id(id)
        return None

    def register_user(
        self, email: str, username: str, password: str, role: str
    ) -> User:
        # Check if account exists alreafy
        if self.get_user_by_email(email) is not None:
            raise UserAuthenticationException(f"User {email} already exists")

        user_id = self._generate_user_id()
        password_encrypted = password  # TODO Encrypt password

        user_obj = User(user_id, username, password_encrypted, email, role, friends=[])
        return self.user_collection.register(user_obj)
    
    # FOR TESTING PURPOSES
    # def make_friends(self):
    #     self.user_collection.create_friendship_using_email("pie8@mail.com", "pie7@mail.com")

    # def remove_friends(self):
        # self.user_collection.remove_friendship_using_email("pie8@mail.com", "pie7@mail.com")
