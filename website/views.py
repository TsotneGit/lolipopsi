from flask import Blueprint, render_template, session, flash, redirect, url_for
from .databases import ProblemsDatabase, UsersDatabase

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    db = ProblemsDatabase("problems.db")
    problems = db.get_all_problems()
    db.close_connection()
    solved = ""
    if session.get("current_user"):
        db_users = UsersDatabase("users.db")
        solved = db_users.get_user(session["current_user"])[4]
        db_users.close_connection()
        solved = set(solved)
    new_problems = []
    for problem in problems:
        new_problems.append(
            [
                str(problem[0]),
                problem[1],
                problem[2],
                problem[3],
                problem[4],
            ]
        )
    return render_template(
        "home.html",
        signed_in=session.get("current_user"),
        problems=new_problems,
        solved=solved,
    )


@views.route("/problem/<prbid>")
def problem(prbid):
    if not session.get("current_user"):
        flash("Please sign in!", category="error")
        return redirect(url_for("views.home"))
    db = ProblemsDatabase("problems.db")
    problem = db.get_problem(prbid)
    db.close_connection()
    problem = list(problem)
    problem[2] = problem[2].split("\n")
    return render_template(
        "problem.html", problem=problem, signed_in=session.get("current_user")
    )
