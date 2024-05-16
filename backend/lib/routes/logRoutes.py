from flask import Flask, redirect, render_template, url_for

from lib.log.log import LogType
from lib.database import MongoDB


def register_log_routes(app: Flask, db: MongoDB):

    @app.route("/logs", methods=["GET"])
    def show_all_logs():
        """
        Retrieves and displays all logs present in the database.

        Returns:
            TemplateResponse: Renders the "logs_template.html" template with the retrieved logs.
        """
        return show_logs(log_type=None)


    @app.route("/logs/", methods=["GET"])
    def redirect_logs_slash():
        """
        Retrieves and displays all logs present in the database.

        Returns:
            TemplateResponse: Renders the "logs_template.html" template with the retrieved logs.
        """
        return redirect(url_for("show_all_logs"))


    @app.route("/logs/<log_type>", methods=["GET"])
    def show_logs(log_type):
        """
        Retrieves and displays logs based on the provided log type.

        Args:
            log_type (str, optional): The type of log to retrieve. Can be one of "INFO", "ERROR", or "CHATBOT". Defaults to None, which retrieves all logs.

        Returns:
            TemplateResponse: Renders the "logs_template.html" template with the provided log type and retrieved logs.

        Raises:
            404: If an invalid log type is provided. (Redirects to "show_all_logs" instead)
        """
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
