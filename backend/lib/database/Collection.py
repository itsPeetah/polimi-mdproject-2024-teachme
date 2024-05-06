"""
Module containing classes for managing collections in the database.
"""

# pylint: disable=line-too-long

from datetime import datetime
from typing import List, Optional
from ..log import LogType
from .data_objects import Conversation, User

class Collection:
    """
    Represents a generic collection in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a Collection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        self._collection = collection
        self._collection_name = collection_name

    @property
    def collection_name(self):
        """
        Get the name of the collection.

        :return: the name of the collection
        :rtype: str
        """
        return self._collection_name


class ConversationsCollection(Collection):
    """
    Represents a collection of conversations in the database.

    Each conversation has the following fields:
    - conversation_id: int
    - user_level: str
    - difficulty: str
    - topic: str
    - teacher_email: str
    - student_email: str
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a ConversationsCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)

    def find_by_id(self, conversation_id: int) -> Conversation:
        """
        Find a conversation by its ID.

        :param conversation_id: ID of the conversation to find
        :type conversation_id: int
        :return: the conversation object
        :rtype: Conversation
        """
        conversation_to_return = self._collection.find_one(
            {"conversation_id": conversation_id}
        )
        return (
            Conversation(**conversation_to_return)
            if conversation_to_return is not None
            else None
        )
    
    def get_user_conversations(self, user_email: str) -> list[Conversation]:
        """
        Returns all the conversations that the user is involved in.
        If the user is a teacher, this method returns all the conversations that the user created.
        If the user is a student, this method returns all the conversations that were assigned to the user.

        Args:
            user_email (str): Email of the student
        
        Returns:
            list[Conversation]: A list of Conversation objects the user is involved in.
        """
        query = {"$or": [
            {"teacher_email": user_email},
            {"student_email": user_email},
        ]}
        conversation_cursor = self._collection.find(query)
        conversations = [Conversation(**conversation) for conversation in conversation_cursor]
        return conversations
    
    def create_conversation(self,
                            user_level: str = None,
                            difficulty: str = None,
                            topic: str = None,
                            teacher_email: str = None,
                            student_email: str = None):
        """
        Creates a new conversation in the database.

        Args:
            user_level (str, optional): Level of the user.
            difficulty (str, optional): Difficulty of the conversation.
            topic (str, optional): Topic of the conversation.
            teacher_email (str, optional): Email of the teacher who created the conversation.
            student_email (str, optional): Email of the student whom the conversation was created for.

        Returns:
            dict: A dictionary containing the details of the created conversation, including the assigned ID (_id) and all other attributes of the Conversation object.
        """

        conversation_dict = {
            "user_level": user_level,
            "difficulty": difficulty,
            "topic": topic,
            "teacher_email": teacher_email,
            "student_email": student_email,
        }
        result = self._collection.insert_one(conversation_dict)

        conversation_dict["_id"] = result.inserted_id

        return conversation_dict

    def insert_one(
        self,
        conversation_id: int,
        user_level: str = None,
        difficulty: str = None,
        topic: str = None,
        teacher_email: str = None,
        student_email: str = None
    ):
        """
        Insert a new conversation into the collection.

        :param conversation_id: ID of the conversation
        :type conversation_id: int
        :param user_level: level of the user, defaults to None
        :type user_level: str, optional
        :param difficulty: difficulty of the conversation, defaults to None
        :type difficulty: str, optional
        :param topic: topic of the conversation, defaults to None
        :type topic: str, optional
        :param teacher_email: email of the teacher who created the conversation, default to None
        :type teacher_email: str, optional
        :param student_email: email of the student whom the conversation was created for, default to None
        :type student_email: str, optional
        """
        conversation = {
            "conversation_id": conversation_id,
            "user_level": user_level,
            "difficulty": difficulty,
            "topic": topic,
            "teacher_email": teacher_email,
            "student_email": student_email,
        }
        self._collection.insert_one(conversation)


class UserDataCollection(Collection):
    """
    Represents a collection of user data in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a UserDataCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)

    def register(self, user: User) -> User:
        self._collection.insert_one(user.__dict__)
        return user
    
    def create_friendship_using_email(self, teacher_email: str, student_email: str):
        """
        Creates a two-way friendship between teacher and student in the database.

        Args:
            teacher_email (str): email of the teacher
            student_email (str): email of the student
        
        Raises:
            ValueError: If teacher or student is not found in the database.
        """

        teacher = self.retrieve_by_email(teacher_email)
        student = self.retrieve_by_email(student_email)

        if not teacher:
            raise ValueError(f"Teacher with email '{teacher_email}' not found")
        if not student:
            raise ValueError(f"Student with email '{student_email}' not found")
        
        existing_friendship = self._collection.find_one({"$or": [{"email": student_email, "friends": teacher_email}, {"email": teacher_email, "friends": student_email}]})
        if existing_friendship:
            print(f"Friendship between {teacher.email} and {student.email} already exists.")
        else:
            update_student = {"$push": {"friends": teacher.email}}
            result_student = self._collection.update_one({"email": student.email}, update_student)

            update_teacher = {"$push": {"friends": student.email}}
            result_teacher = self._collection.update_one({"email": teacher.email}, update_teacher)

            if result_student.matched_count > 0 and result_teacher.matched_count > 0:
                print(f"Successfully created friendship between {teacher.email} and {student.email}")
            else:
                print(f"An error occurred while creating friendship between {teacher.email} and {student.email}")

    def create_friendship_using_id(self, teacher_id: str, student_id: str):
        """
        Creates a two-way friendship between teacher and student in the database.

        Args:
            teacher_id (str): id of the teacher
            student_id (str): id of the student
        
        Raises:
            ValueError: If teacher or student is not found in the database.
        """

        teacher = self.retrieve_by_id(teacher_id)
        student = self.retrieve_by_id(student_id)

        if not teacher:
            raise ValueError(f"Teacher with id '{teacher_id}' not found")
        if not student:
            raise ValueError(f"Student with id '{student_id}' not found")
        
        self.create_friendship(teacher.email, student.email)

    def remove_friendship_using_email(self, teacher_email: str, student_email: str):
        """
        Removes friendship between teacher and student.

        Args:
            teacher_email (str): email of the teacher
            student_email (str): email of the student
        
        Raises:
            ValueError: If teacher or student is not found in the database.
        """
        teacher = self.retrieve_by_email(teacher_email)
        student = self.retrieve_by_email(student_email)

        if not teacher:
            raise ValueError(f"Teacher with email '{teacher_email}' not found")
        if not student:
            raise ValueError(f"Student with email '{student_email}' not found")
        
        update_student = {"$pull": {"friends": teacher.email}}
        update_teacher = {"$pull": {"friends": student.email}}

        result_student = self._collection.update_one({"email": student.email}, update_student)
        result_teacher = self._collection.update_one({"email": teacher.email}, update_teacher)

        if (result_student.matched_count > 0 or result_teacher.matched_count > 0) and (result_student.modified_count > 0 or result_teacher.modified_count > 0):
            print(f"Successfully removed friendship between {teacher.email} and {student.email}")
        else:
            print(f"No friendship found to remove.")

    def remove_friendship_using_id(self, teacher_id: str, student_id: str):
        """
        Removes friendship between teacher and student.

        Args:
            teacher_id (str): id of the teacher
            student_id (str): id of the student
        
        Raises:
            ValueError: If teacher or student is not found in the database.
        """
        teacher = self.retrieve_by_id(teacher_id)
        student = self.retrieve_by_id(student_id)

        if not teacher:
            raise ValueError(f"Teacher with id '{teacher_id}' not found")
        if not student:
            raise ValueError(f"Student with id '{student_id}' not found")
        
        self.remove_friendship_using_email(teacher.email, student.email)
    
    def get_user_friends(self, user_email: str) -> List[User]:
        """
        Returns all the friends of the user.
        If the user is a teacher, this method returns all the teacher's students.
        If the user is a student, this method returns all the student's teachers.

        Args:
            user_email (str): email of the student
        """
        user = self.retrieve_by_email(user_email)

        if not user:
            raise ValueError(f"User with email {user_email} not found")
        
        friends_cursor = self._collection.find({"email": {"$in": user.friends}})
        friends = []
        for friend in friends_cursor:
            user = self.retrieve_by_email(friend)
            if user:
                friends.append(user)
        return friends
        
    def retrieve_by_id(self, user_id: str) -> Optional[User]:
        user = self._collection.find_one({"_id": user_id})
        if not user:
            return None
        return User(**user)

    def retrieve_by_email(self, email: str) -> User:
        user = self._collection.find_one({"email": email})
        if not user:
            return None
        return User(**user)


class ChatMessageHistoryCollection(Collection):
    """
    Represents a collection of chat message history in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a ChatMessageHistoryCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)

class LogsCollection(Collection):
    """
    Represents a collection of logs in the database.
    """
    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a LogsCollection object.

        :param collection: the collection object from the database
        :type collection: any
        :param collection_name: name of the collection
        :type collection_name: str
        """
        super().__init__(collection, collection_name)
    
    def retrieve_all(self):
        return list(self._collection.find({}))
    
    def retrieve_by_log_type(self, log_type: LogType):
        return list(self._collection.find({"log_type": log_type.value}))
    
    def insert_one(self, log_type: LogType, message: str, time_stamp: datetime = None):
        """
        Insert a new conversation into the collection.

        :param log_type: type of the log
        :type log_type: LogType
        :param message: message of the log
        :type message: str
        :param time_stamp: timestamp of the log
        :type time_stamp: datetime
        """
        log = {
            "log_type": log_type.value,
            "message": message,
            "time_stamp": time_stamp,
        }
        self._collection.insert_one(log)

class CollectionDispatcher():
    """
    Dispatcher class for managing collections in the database.
    """

    def __init__(self, collection_names: List[str], db) -> None:
        """
        Initialize a CollectionDispatcher object.

        :param collection_names: list of collection names
        :type collection_names: List[str]
        :param db: the database object
        :type db: any
        """
        self._connection_names = collection_names
        self._db = db

    def get_collection(self, collection_name: str):
        """Return the collection object for the given collection name.

        :param collection_name: name of the collection to be returned
        :type collection_name: str
        :raises KeyError: if the collection name is not found in the database
        :return: the collection object
        :rtype: Collection
        """
        if collection_name not in self._connection_names:
            raise KeyError(f"Collection {collection_name} not found in the database.")

        # switching to the correct collection
        if collection_name == "conversations":
            return ConversationsCollection(self._db[collection_name], collection_name)
        elif collection_name == "user_data":
            return UserDataCollection(self._db[collection_name], collection_name)
        elif collection_name=='chat_message_history':
            return ChatMessageHistoryCollection(self._db[collection_name], collection_name)
        elif collection_name=='logs':
            return LogsCollection(self._db[collection_name], collection_name)
        else:
            return Collection(self._db[collection_name], collection_name)
