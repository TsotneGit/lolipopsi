from flask import Blueprint, redirect, request, flash, url_for, session
from .tester import test_solution
from .databases import UsersDatabase


submit_solution = Blueprint("submit_solution", __name__)


@submit_solution.route("/<prbid>", methods=["GET", "POST"])
def submit(prbid):
    if request.method == "POST":
        try:
            code = request.form.get("code")
            if test_solution(prbid, code):
                db = UsersDatabase("users.db")
                db.solve(session["current_user"], prbid)
                db.close_connection()
                flash("Accepted!", category="success")
                return redirect(url_for("views.problem", prbid=prbid))
            else:
                flash("Wrong answer!", category="error")
                return redirect(url_for("views.problem", prbid=prbid))
        except:
            flash("Runtime error!", category="error")
            return redirect(url_for("views.problem", prbid=prbid))
    flash("Wrong answer!", category="error")
    return redirect(url_for("views.problem", prbid=prbid))
