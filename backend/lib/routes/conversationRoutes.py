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
        conv = conversations_collection.create_conversation(
            user_level=user_level,
            difficulty=difficulty,
            topic=topic,
            teacher_email=teacher_email,
            student_email=student_email,
            time_limit=time_limit,
        )

        return jsonify({"conversation_id": str(conv._id)})

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

    @app.route("/foochatbot", methods=["GET"])
    def foo():
        return make_response(str(len(cbm.chatbots)), 200)
