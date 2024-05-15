import os

from flask import Flask, request, jsonify, make_response

from lib.log import LogType, Logger, Log
from lib.database import MongoDB
from lib.llm import ConversationalChatBot, ChatbotManager

active_conversations = {}


def register_conversation_routes(
    app: Flask, db: MongoDB, cbm: ChatbotManager, logger: Logger = None
):

    @app.route("/create-conversation", methods=["POST"])
    def create_conversation():
        data = request.get_json()
        user_level = data.get("user_level")
        difficulty = data.get("difficulty")
        topic = data.get("topic")
        teacher_email = data.get("teacher_email")
        student_email = data.get("student_email")
        time_limit = data.get("time_limit")
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
        data = request.get_json()
        conversation_id = data.get("conversation_id")

        (status_code, response) = cbm.init_chatbot(conversation_id, db, logger)

        return make_response(response, status_code)

    @app.route("/user-chat-message", methods=["POST"])
    def user_chat_message():
        data = request.get_json()
        conversation_id = data.get("conversation_id")

    @app.route("/foochatbot", methods=["GET"])
    def foo():
        return make_response(str(len(cbm.chatbots)), 200)
