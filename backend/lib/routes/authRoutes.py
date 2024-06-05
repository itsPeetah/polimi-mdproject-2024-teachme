from flask import Flask, jsonify, make_response, request
from ..auth.AuthenticationService import (
    AuthenticationService,
    UserAuthenticationException,
)


def register_auth_routes(app: Flask, user_auth: AuthenticationService):

    @app.route("/register", methods=["POST"])
    def handle_sign_up():
        """
        Endpoint for user registration.

        This endpoint is accessed via a POST request and is used for user sign-up.
        It validates the request data, registers a new user, and returns a response
        with the user ID. Additionally, it sets a cookie to maintain the session.

        Returns:
            Response: A JSON response containing the user's ID if the registration
            is successful. A cookie named "uid" is set with the user's ID and a max age of 10 days.
            If registration fails, a response with status code 400 and message "KO" is returned.
        """
        try:
            request_data = user_auth.validate_request_data(request, signup=True)
            user = user_auth.register_user(**request_data)
            response = jsonify({"uid": user._id})
            response.set_cookie(key="uid", value=user._id, max_age=60 * 60 * 24 * 10)
            return response
        except UserAuthenticationException as ex:
            print(ex)
            return make_response("KO", 400)

    @app.route("/login", methods=["POST"])
    def handle_sign_in():
        """
        Endpoint for user sign-in.

        This endpoint is accessed via a POST request and is used for user authentication.
        It validates the request data, checks the user's credentials, and returns a response
        with the user ID and role. Additionally, it sets a cookie to maintain the session.

        Returns:
            Response: A JSON response containing the user's ID and role if the authentication
            is successful. A cookie named "uid" is set with the user's ID and a max age of 10 days.
            If authentication fails, a response with status code 400 and message "KO" is returned.
        """
        try:
            request_data = user_auth.validate_request_data(request, signup=False)
            user = user_auth.get_user_by_email(request_data["email"])
            response = jsonify({"uid": user._id, "role": user.role})
            response.set_cookie(key="uid", value=user._id, max_age=60 * 60 * 24 * 10)
            return response
        except UserAuthenticationException as ex:
            return make_response("KO", 400)

    @app.route("/me", methods=["GET"])
    def handle_is_logged_in():
        """
        Endpoint to check if a user is logged in and return their details.

        This endpoint is accessed via a GET request and checks for the presence of a
        "uid" cookie to identify the user. If the user is authenticated, their user
        details, including user ID, email, and role, are returned in a JSON response.

        Returns:
            Response: A JSON response containing the user's ID, email, and role if
            the user is authenticated. If the user is not authenticated or any error
            occurs, a response with status code 400 and message "KO" is returned.
        """
        try:
            uid = request.cookies["uid"]
            user = user_auth.get_user_by_id(uid)
            return jsonify({"user_id": user._id, "user_email": user.email, "role": user.role})
        except:
            return make_response("KO", 400)
