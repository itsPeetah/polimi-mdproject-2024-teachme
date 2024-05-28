from datetime import datetime
import os

from flask import Flask, request, jsonify, make_response

from lib.log import LogType, Logger, Log
from lib.database import MongoDB
from lib.llm import ConversationalChatBot, ChatbotManager


def register_conversation_routes(
    app: Flask, db: MongoDB, cbm: ChatbotManager, logger: Logger = None
):

    @app.route("/create-conversation", methods=["POST"])
    def create_conversation():
        """
        Creates a new conversation in the database.

        Request Parameters:
        * user_level (required, string): Level of the user. Possible values: "beginner", "intermediate", "advanced".
        * difficulty (required, string): Difficulty of the conversation. Possible values: "easy", "medium", "challenging".
        * topic (optional, string): Topic of the conversation. Defaults to None.
        * teacher_email (required, string): Email address of the teacher who created the conversation.
        * student_email (required, string): Email address of the student whom the conversation was assigned to.
        * time_limit (optional, string or int): Time limit of the conversation (in minutes). Defaults to 5 minutes.

        Returns (Response):
        The function returns the simple message "Ok" upon successful creation of the conversation.
        """
        data = request.get_json()
        user_level = data.get("user_level")
        difficulty = data.get("difficulty")
        topic = data.get("topic")
        teacher_email = data.get("teacher_email")
        student_email = data.get("student_email")
        time_limit_temp = data.get("time_limit")
        if isinstance(time_limit_temp, str) and time_limit_temp.isdigit():
            time_limit = int(time_limit_temp)
        else:
            time_limit = time_limit_temp

        conversations_collection = db.get_collection("conversations")
        managed_conversations_collection = db.get_collection(
            "managed_conversations")
        conv = conversations_collection.create_conversation(
            user_level=user_level,
            difficulty=difficulty,
            topic=topic,
            teacher_email=teacher_email,
            student_email=student_email,
            time_limit=time_limit,
        )
        managed_conversations_collection.create_managed_conversation(
            conversation_id=str(conv._id),
        )

        return jsonify({"conversation_id": str(conv._id)})

    @app.route("/list-user-conversations/<user_email>", methods=["GET"])
    def list_user_conversations(user_email):
        """
        Returns the ids of all the conversations that the user is involved in.
        If the user is a teacher, this method returns all the conversations that the user created.
        If the user is a student, this method returns all the conversations that were assigned to the user.

        Args:
            user_email (required, string): Email of the user

        Returns (Response):
            A JSON file containing the ids of all the conversations that the user is involed in.
            If a problem occurs, the function returns error 400.
        """
        conversations_collection = db.get_collection("conversations")
        if user_email is not None:
            conversations = conversations_collection.get_user_conversations(
                user_email=user_email)
            return jsonify(conversations)
        else:
            return make_response(400, "The user email was not specified.")

    @app.route("/get-conversation-info/<conversation_id>", methods=["GET"])
    def get_conversation_info(conversation_id):
        """
        Returns information about the conversation with the specified id.

        Args:
            conversation_id (required, string): id of the conversation.

        Return (Response):
            A JSON containing the information about the conversation with the specified id. If a problem occurs, the funtion returns error 400.
        """
        conversations_collection = db.get_collection("conversations")
        if conversation_id is not None:
            conversation = conversations_collection.find_by_id(
                conversation_id=conversation_id)
            conversation._id = str(conversation._id)
            return jsonify(conversation)
        else:
            return make_response(400, "The conversation id was not specified.")

    @app.route("/initialize-conversation", methods=["POST"])
    def initialize_conversation():
        """
        Initializes an already existing conversation. This is necessary in order to load the corresponding chatbot from the conversation in the database.

        Request Parameters:
        * conversation_id (required, string): The unique identifier of the conversation.

        Returns (Response):
        The function returns the code 200 and the message "Conversation initialized successfully" upon successful creation of the conversation. If an error occurs, it returns the code 400 with a message specifying the error.
        """
        data = request.get_json()
        conversation_id = data.get("conversation_id")

        (status_code, response) = cbm.init_chatbot(conversation_id, db, logger)

        return make_response(response, status_code)

    @app.route("/user-chat-message", methods=["POST"])
    def user_chat_message():
        """
        Handles user messages sent to the specified chatbot, through a POST request.

        Request Parameters:
        * conversation_id (required, string): The unique identifier of the conversation.
        * sender_id (required, string): The unique identifier of the user who sends the message.
        * message (required, string): The text message sent by the user.

        Returns (Response):
        A JSON object with the following properties:
        * conversation_id (string): The conversation ID (same as the request parameter).
        * response (string): The chatbot's response to the user message.
        """
        data = request.get_json()
        conversation_id = data.get("conversation_id")
        sender_id = data.get("sender_id")
        message = data.get("message")

        status_code, response = cbm.send_message_to_chatbot(
            cid=conversation_id, message=message)

        return make_response(jsonify({"conversation_id": conversation_id, "response": response}), status_code)

    @app.route("/end-conversation/<conversation_id>", methods=["GET"])
    def end_conversation():
        """
        Ends the conversation with the specified id.

        Args:
            conversation_id (required, string): id of the conversation.

        Returns (Response):
            The function returns the code 200 and the message "Conversation ended successfully" upon successful ending of the conversation. If an error occurs, it returns the code 400 with a message specifying the error.
        """
        conversation_id = request.args.get("conversation_id")

        (status_code, response) = cbm.end_chatbot(conversation_id, db, logger)

        return make_response(response, status_code)

    @app.route("/foochatbot", methods=["GET"])
    def foo():
        return make_response(str(len(cbm.chatbots)), 200)
