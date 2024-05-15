from flask import Flask, request

from lib.log.log import LogType
from lib.database import MongoDB


def register_conversation_routes(app: Flask, db: MongoDB):

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
            time_limit=time_limit
        )
        return "Ok"
