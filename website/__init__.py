from flask import Flask
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=6)

    from .views import views
    from .auth import auth
    from .submit_solution import submit_solution

    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_blueprint(submit_solution, url_prefix="/submit_solution")

    return app
