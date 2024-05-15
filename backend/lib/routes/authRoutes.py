from flask import Flask, jsonify, make_response, request
from ..auth.AuthenticationService import (
    AuthenticationService,
    UserAuthenticationException,
)


def register_auth_routes(app: Flask, user_auth: AuthenticationService):

    @app.route("/register", methods=["POST"])
    def handle_sign_up():
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
        try:
            request_data = user_auth.validate_request_data(request, signup=False)
            user = user_auth.get_user_by_email(request_data["email"])
            response = jsonify({"uid": user._id})
            response.set_cookie(key="uid", value=user._id, max_age=60 * 60 * 24 * 10)
            return response
        except UserAuthenticationException as ex:
            return make_response("KO", 400)

    @app.route("/me", methods=["GET"])
    def handle_is_logged_in():
        # TODO Add Role differentiation
        try:
            uid = request.cookies["uid"]
            user = user_auth.get_user_by_id(uid)
            return jsonify({"user_id": user._id, "role": user.role})
        except:
            return make_response("KO", 400)
