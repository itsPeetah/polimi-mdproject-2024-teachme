from flask import Flask, redirect, render_template, url_for

from lib.log.log import LogType
from lib.database.Database import MongoDB


def register_log_routes(app: Flask, db: MongoDB):

    @app.route("/logs", methods=["GET"])
    def show_all_logs():
        return show_logs(log_type=None)

    @app.route("/logs/", methods=["GET"])
    def redirect_logs_slash():
        return redirect(url_for("show_all_logs"))

    @app.route("/logs/<log_type>", methods=["GET"])
    def show_logs(log_type):
        logs_collection = db.get_collection("logs")
        if log_type is None:
            logs = logs_collection.retrieve_all()
        else:
            log_type = log_type.upper()
            if log_type == "INFO":
                logs = logs_collection.retrieve_by_log_type(LogType.INFO)
            elif log_type == "ERROR":
                logs = logs_collection.retrieve_by_log_type(LogType.ERROR)
            elif log_type == "CHATBOT":
                logs = logs_collection.retrieve_by_log_type(LogType.CHATBOT)
            else:
                return redirect(url_for("show_all_logs"))
        return render_template("logs_template.html", log_type=log_type, logs=logs)
