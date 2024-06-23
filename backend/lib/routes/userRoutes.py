from flask import Flask, jsonify, make_response, request

from lib.log import Log, LogType, Logger
from lib.database import MongoDB


def register_user_routes(app: Flask, db: MongoDB, logger: Logger):
    @app.route("/create-friendship", methods=["POST"])
    def create_friendship():
        """
        Creates a friendship between a teacher and a student in the database.

        Request parameters:
            teacher_email (str): The email of the teacher.
            student_email (str): The email of the student.
        
        Example request body:
        {
            "teacher_email": "teacher@example.com",
            "student_email": "student@example.com"
        }
        
        Returns:
            str: "Ok" if the friendship was successfully created.
        """
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
        """
        Removes a friendship between a teacher and a student in the database.

        Request parameters:
            teacher_email (str): The email of the teacher.
            student_email (str): The email of the student.

        Example request body:
            {
                "teacher_email": "teacher@example.com",
                "student_email": "student@example.com"
            }

        Returns:
            str: "Ok" if the friendship was successfully removed.
        """
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
        """
        Retrieves all the friends of the user. If the user is a teacher, this returns all the teacher's students. If the user is a student, this returns all the student's teachers.

        Args:
            user_email (str): The email of the user.
        
        Returns:
            Response:
                - JSON containing the friends of the user if the request is successful.
                - 400 status code with an error message if the user was not found.
        """
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
        """
        Retrieves all the students registered in the database.

        Returns:
            Response:
                - JSON containing a list of dictionaries, each containing the email address, username, and id of a student.

        Response example:
            [
                {
                    "_id": "cd70b6d8-d393-487b-9faf-aeaa10904349",
                    "email": "student1@mail.com",
                    "username": "student_one"
                },
                {
                    "_id": "07c291ac-74e5-4bda-95f2-319800ed70b2",
                    "email": "student2@mail.com",
                    "username": "student_two"
                }
            ]
        """
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
