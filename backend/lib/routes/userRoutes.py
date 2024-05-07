from flask import Flask, jsonify, make_response, request

from lib.log import Log, LogType, Logger
from lib.database import MongoDB


def register_user_routes(app: Flask, db: MongoDB, logger: Logger):
    @app.route("/create-friendship", methods=["POST"])
    def create_friendship():
        data = request.get_json()
        teacher_email = data.get("teacher_email")
        student_email = data.get("student_email")
        # db = app_db_connector.connect("teachme_main")
        user_data_collection = db.get_collection("user_data")
        user_data_collection.create_friendship_using_email(
            teacher_email=teacher_email, student_email=student_email
        )  # TODO: add better error management
        return "Ok"

    @app.route("/remove-friendship", methods=["POST"])
    def remove_friendship():
        data = request.get_json()
        teacher_email = data.get("teacher_email")
        student_email = data.get("student_email")
        # db = app_db_connector.connect("teachme_main")
        user_data_collection = db.get_collection("user_data")
        user_data_collection.remove_friendship_using_email(
            teacher_email=teacher_email, student_email=student_email
        )  # TODO: add better error management
        return "Ok"

    @app.route("/get-friends/<user_email>", methods=["GET"])
    def get_friends(user_email: str):
        # data = request.get_json()
        # user_email = data.get("user_email")
        # db = app_db_connector.connect("teachme_main")
        logger.log(
            Log(
                LogType.INFO,
                f"Received GET request at /get-friends/ for user_email: {user_email}",
            )
        )
        if user_email is None:
            return make_response(400, "KO")
        user_data_collection = db.get_collection("user_data")
        user_friends = user_data_collection.get_user_friends(user_email=user_email)
        return jsonify(user_friends)
