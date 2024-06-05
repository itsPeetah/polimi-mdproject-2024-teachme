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
        user_friends = user_data_collection.get_user_friends(
            user_email=user_email)
        return jsonify(user_friends)

    @app.route("/get-all-students", methods=["GET"])
    def get_all_students():
        user_data_collection = db.get_collection("user_data")
        students = user_data_collection.get_all_students()
        return make_response(jsonify(students), 200)

    @app.route("/get-username/<user_email>", methods=["GET"])
    def get_username(user_email: str):
        """
        Get the username and friends of a user by their email.

        Args:
            user_email (str): The email of the user.

        Returns:
            Response:
                - JSON containing the username and friends of the user if the request is successful.
                - 400 status code with an error message if the email is missing or the user does not exist.

        """
        user_data_collection = db.get_collection("user_data")
        user = user_data_collection.retrieve_by_email(user_email)
        if user is not None:
            response = {
                "username": user.username,
                "friends": user.friends
            }

            return make_response(jsonify(response), 200)
        else:
            return make_response("The user with the specified email does not exist.", 400)
