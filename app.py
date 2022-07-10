from website import create_app
from website.problem_reader import add_problems_to_database
import os


def runapp():
    app = create_app()
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    if os.path.exists("problems.db"):
        os.remove("problems.db")
    add_problems_to_database()
    runapp()
