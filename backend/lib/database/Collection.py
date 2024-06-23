"""
Module containing classes for managing collections in the database.
"""

# pylint: disable=line-too-long

from datetime import datetime
from typing import List, Optional
from bson.objectid import ObjectId

from ..log import LogType
from .data_objects import Conversation, User, ManagedConversation


class Collection:
    """
    Represents a generic collection in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a Collection object.

        Args:
            collection (any): The collection object from the database.
            collection_name (str): The name of the collection.
        """
        self._collection = collection
        self._collection_name = collection_name

    @property
    def collection_name(self):
        """
        Get the name of the collection.

        Args:
            None

        Returns:
            str: The name of the collection.
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
    - time_limit: int
    - is_ended: bool
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a ConversationsCollection object.

        Args:
            collection (any): The collection object from the database.
            collection_name (str): The name of the collection.
        """
        super().__init__(collection, collection_name)

    def find_by_id(self, conversation_id: str) -> Conversation:
        """
        Find a conversation by its ID.

        Args:
            conversation_id (str): ID of the conversation to find

        Returns:
            Conversation: The conversation object
        """
        conversation_to_return = self._collection.find_one(
            {"_id": ObjectId(conversation_id)}
        )
        return (
            Conversation(**conversation_to_return)
            if conversation_to_return is not None
            else None
        )

    def get_user_conversations(self, user_email: str) -> list[str]:
        """
        Returns the ids of all the conversations that the user is involved in.
        If the user is a teacher, this method returns all the conversations that the user created.
        If the user is a student, this method returns all the conversations that were assigned to the user.

        Args:
            user_email (str): Email of the user

        Returns:
            list[dict]: A list of the conversations that the user is involved in.
        """
        query = {
            "$or": [
                {"teacher_email": user_email},
                {"student_email": user_email},
            ]
        }
        conversation_cursor = self._collection.find(query)

        conversations = [
            {
                "_id": str(conversation["_id"]),
                "user_level": conversation["user_level"],
                "difficulty": conversation["difficulty"],
                "topic": conversation["topic"],
                "teacher_email": conversation["teacher_email"],
                "student_email": conversation["student_email"],
                "is_ended": conversation["is_ended"],
                "time_limit": conversation["time_limit"],
            }
            for conversation in conversation_cursor
        ]
        return conversations

    def create_conversation(
        self,
        user_level: str = None,
        difficulty: str = None,
        topic: str = None,
        teacher_email: str = None,
        student_email: str = None,
        is_ended: bool = False,
        time_limit: int = 5,
        parent_conversation_id: str = None,
    ):
        """
        Creates a new conversation in the database.

        Args:
            user_level (str, optional): Level of the user. Defaults to None.
            difficulty (str, optional): Difficulty of the conversation. Defaults to None.
            topic (str, optional): Topic of the conversation. Defaults to None.
            teacher_email (str, optional): Email of the teacher who created the conversation. Defaults to None.
            student_email (str, optional): Email of the student whom the conversation was created for. Defaults to None.
            is_ended (bool, optional): Whether the conversation is currently ended or not. Defaults to False.
            time_limit (int, optional): Time limit for the conversation expressed in minutes. Defaults to 5.

        Returns:
            dict: A dictionary containing the details of the created conversation, including the assigned ID (_id) and all other attributes of the Conversation object.
        """

        conversation_dict = {
            "user_level": user_level,
            "difficulty": difficulty,
            "topic": topic,
            "teacher_email": teacher_email,
            "student_email": student_email,
            "is_ended": is_ended,
            "time_limit": time_limit,
            "parent_conversation_id": parent_conversation_id,
        }
        result = self._collection.insert_one(conversation_dict)

        conversation_dict["_id"] = result.inserted_id

        return Conversation(**conversation_dict)

    def end_conversation(self, conversation_id: str):
        """
        Ends a conversation by setting the is_ended attribute to True.

        Args:
            conversation_id (str): ID of the conversation to end.
        """
        res = self._collection.update_one(
            {"_id": ObjectId(conversation_id)}, {"$set": {"is_ended": True}}
        )

        if res.matched_count == 0:
            raise ValueError(f"Conversation with id {conversation_id} not found.")


class UserDataCollection(Collection):
    """
    Represents a collection of user data in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a UserDataCollection object.

        Args:
            collection (any): the collection object from the database
            collection_name (str): name of the collection

        Returns:
            None
        """
        super().__init__(collection, collection_name)

    def register(self, user: User) -> User:
        """
        Register a new user in the database.

        Args:
            user (User): The user object to be registered.

        Returns:
            User: The registered user object.
        """
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

        existing_friendship = self._collection.find_one(
            {
                "$or": [
                    {"email": student_email, "friends": teacher_email},
                    {"email": teacher_email, "friends": student_email},
                ]
            }
        )
        if existing_friendship:
            print(
                f"Friendship between {teacher.email} and {student.email} already exists."
            )
        else:
            update_student = {"$push": {"friends": teacher.email}}
            result_student = self._collection.update_one(
                {"email": student.email}, update_student
            )

            update_teacher = {"$push": {"friends": student.email}}
            result_teacher = self._collection.update_one(
                {"email": teacher.email}, update_teacher
            )

            if result_student.matched_count > 0 and result_teacher.matched_count > 0:
                print(
                    f"Successfully created friendship between {teacher.email} and {student.email}"
                )
            else:
                print(
                    f"An error occurred while creating friendship between {teacher.email} and {student.email}"
                )

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

        self.create_friendship_using_email(teacher.email, student.email)

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

        result_student = self._collection.update_one(
            {"email": student.email}, update_student
        )
        result_teacher = self._collection.update_one(
            {"email": teacher.email}, update_teacher
        )

        if (result_student.matched_count > 0 or result_teacher.matched_count > 0) and (
            result_student.modified_count > 0 or result_teacher.modified_count > 0
        ):
            print(
                f"Successfully removed friendship between {teacher.email} and {student.email}"
            )
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

    def get_user_friends(self, user_email: str) -> list[str]:
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

        return user.friends

    def get_all_students(self) -> list[dict]:
        """
        Returns all the students in the database.

        :return: A list of all the students in the database.
        :rtype: list[dict]
        """
        students_cursor = self._collection.find({"role": "student"})
        students = []
        for student in students_cursor:
            students.append(
                {
                    "_id": str(student["_id"]),
                    "username": student["username"],
                    "email": student["email"],
                }
            )
        return students

    def retrieve_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by its ID.

        :param user_id: the ID of the user to retrieve
        :type user_id: str
        :return: the user object
        :rtype: Optional[User]
        """
        user = self._collection.find_one({"_id": user_id})
        if not user:
            return None
        return User(**user)

    def retrieve_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by its email.

        :param email: the email of the user to retrieve
        :type email: str
        :return: the user object
        :rtype: Optional[User]
        """
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

        Args:
            collection (any): the collection object from the database
            collection_name (str): name of the collection
        """
        super().__init__(collection, collection_name)


class LogsCollection(Collection):
    """
    Represents a collection of logs in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a LogsCollection object.

        Args:
            collection (any): the collection object from the database
            collection_name (str): name of the collection

        Returns:
            None
        """
        super().__init__(collection, collection_name)

    def retrieve_all(self):
        return list(self._collection.find({}))

    def retrieve_by_log_type(self, log_type: LogType):
        return list(self._collection.find({"log_type": log_type.value}))

    def insert_one(self, log_type: LogType, message: str, time_stamp: datetime = None):
        """
        Insert a new conversation into the collection.

        Args:
            log_type (LogType): Type of the log.
            message (str): Message of the log.
            time_stamp (datetime): Timestamp of the log.

        Returns:
            None
        """
        log = {
            "log_type": log_type.value,
            "message": message,
            "time_stamp": time_stamp,
        }
        self._collection.insert_one(log)


class ManagedConversationsCollection(Collection):
    """
    Represents a collection of ended conversations in the database.
    """

    def __init__(self, collection, collection_name: str) -> None:
        """
        Initialize a EndedConversationsCollection object.

        Args:
            collection (any): The collection object from the database.
            collection_name (str): The name of the collection.

        Returns:
            None
        """
        super().__init__(collection, collection_name)

    def create_managed_conversation(
        self,
        conversation_id: str,
        messages: list = None,
        reversed_role_prompt: str = None,
        overall_feedback: str = None,
    ) -> ManagedConversation:
        """
        Creates a new managed conversation in the database.

        A managed conversation is a structured conversation object that keeps track of the messages exchanged between the user and the chatbot. The user messages are stored with additional information for post conversation analysis.

        Args:
            conversation_id (str): ID of the conversation. Equal to the conversation id in the conversations collection.
            messages (list, optional): List of messages exchanged between the user and the chatbot. Defaults to None.
            reversed_role_prompt (str, optional): The prompt for the reversed role challenge conversation. Defaults to None.
            overall_feedback (str, optional): The overall feedback for the conversation. Defaults to None.

        Returns:
            ManagedConversation: The managed conversation object created in the database.
        """
        managed_conversation_object = {
            "_id": ObjectId(conversation_id),
            "messages": messages if messages is not None else [],
            "role_reversed_prompt": (
                reversed_role_prompt if reversed_role_prompt is not None else ""
            ),
            "overall_feedback": (
                overall_feedback if overall_feedback is not None else ""
            ),
        }
        self._collection.insert_one(managed_conversation_object)
        return ManagedConversation(**managed_conversation_object)

    def add_message(self, conversation_id: str, message: dict) -> None:
        """
        Add a message to the managed conversation.

        Args:
            conversation_id (str): ID of the conversation. Equal to the conversation id in the conversations collection.
            message (dict): The message to add to the conversation.

        Returns:
            None
        """
        try:
            self._collection.update_one(
                {"_id": ObjectId(conversation_id)}, {"$push": {"messages": message}}
            )
        except KeyError:
            print(f"Conversation with id {conversation_id} not found.")

    def get_by_id(self, conversation_id: str) -> ManagedConversation:
        """
        Retrieve a managed conversation by its ID.

        Args:
            conversation_id (str): ID of the conversation. Equal to the conversation id in the conversations collection.

        Returns:
            ManagedConversation: The managed conversation object.

        """
        managed_conversation = self._collection.find_one(
            {"_id": ObjectId(conversation_id)}
        )
        return (
            ManagedConversation(**managed_conversation)
            if managed_conversation is not None
            else None
        )

    def get_formatted_conversation_string(self, conversation_id: str) -> str:
        """
        Retrieve the formatted conversation string for the given conversation ID.

        Args:
            conversation_id (str): ID of the conversation. Equal to the conversation id in the conversations collection.

        Returns:
            str: The formatted conversation string.
        """
        managed_conversation = self.get_by_id(conversation_id)
        if managed_conversation is None:
            return ""

        conversation_string = ""
        for message in managed_conversation.messages:
            if message["role"] == "ai":
                conversation_string += (
                    f"Conversational partner message: {message['message_content']}\n"
                )
            else:
                conversation_string += f"User message: {message['message_content']}\n"
        return conversation_string

    def set_overall_feedback(self, conversation_id: str, overall_feedback: str) -> None:
        """
        Set the overall feedback for the conversation.

        Args:
            conversation_id (str): ID of the conversation. Equal to the conversation id in the conversations collection.
            overall_feedback (str): The overall feedback for the conversation.

        Returns:
            None
        """
        self._collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"overall_feedback": overall_feedback}},
        )

    def set_user_opinion_summary(self, conversation_id: str, user_summary: str) -> None:
        """
        Set the overall feedback for the conversation.

        Args:
            conversation_id (str): ID of the conversation. Equal to the conversation id in the conversations collection.
            overall_feedback (str): The overall feedback for the conversation.

        Returns:
            None
        """
        self._collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"role_reversed_prompt": user_summary}},
        )


class CollectionDispatcher:
    """
    Dispatcher class for managing collections in the database.
    """

    def __init__(self, collection_names: List[str], db) -> None:
        """
        Initialize a CollectionDispatcher object.

        Args:
            collection_names (List[str]): List of collection names.
            db (any): The database object.

        Raises:
            KeyError: If the collection name is not found in the database.

        Returns:
            None
        """
        self._connection_names = collection_names
        self._db = db

    def get_collection(self, collection_name: str):
        """
        Return the collection object for the given collection name.

        Args:
            collection_name (str): Name of the collection to be returned.

        Raises:
            KeyError: If the collection name is not found in the database.

        Returns:
            Collection: The collection object.
        """
        if collection_name not in self._connection_names:
            raise KeyError(f"Collection {collection_name} not found in the database.")

        # switching to the correct collection
        if collection_name == "conversations":
            return ConversationsCollection(self._db[collection_name], collection_name)
        elif collection_name == "user_data":
            return UserDataCollection(self._db[collection_name], collection_name)
        elif collection_name == "chat_message_history":
            return ChatMessageHistoryCollection(
                self._db[collection_name], collection_name
            )
        elif collection_name == "logs":
            return LogsCollection(self._db[collection_name], collection_name)
        elif collection_name == "managed_conversations":
            return ManagedConversationsCollection(
                self._db[collection_name], collection_name
            )
        else:
            return Collection(self._db[collection_name], collection_name)
