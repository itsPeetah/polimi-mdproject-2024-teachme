import os

from bson.errors import InvalidId

from flask import Flask, request

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
        conversations_collection.create_conversation(
            user_level=user_level,
            difficulty=difficulty,
            topic=topic,
            teacher_email=teacher_email,
            student_email=student_email,
            time_limit=time_limit,
        )
        return "Ok"

    @app.route("/initialize-conversation", methods=["POST"])
    def initialize_conversation():
        data = request.get_json()
        conversation_id = data.get("conversation_id")

        conversations_collection = db.get_collection("conversations")

        try:
            conversation = conversations_collection.find_by_id(conversation_id)
        except InvalidId:
            logger.log(
                Log(LogType.ERROR, f"Invalid conversation_id: {conversation_id}")
            )
            return "Invalid conversation_id"

        if conversation is None:
            logger.log(Log(LogType.ERROR, f"Conversation not found: {conversation_id}"))
            return "Conversation not found. You must create a conversation before initializing it."

        # Initializing the Chatbot for the conversation if not already initialized
        if conversation_id not in active_conversations:
            active_conversations[conversation_id] = {
                "conversation": conversation,
                "chatbot": ConversationalChatBot(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    conversation_id=conversation_id,
                    db_connector=db,
                    db_name="teachme_main",
                    logger=logger,
                ),
            }
        else:
            logger.log(
                Log(
                    log_type=LogType.INFO,
                    message=f"Conversation {conversation_id} already initialized",
                )
            )

        return "Ok"
