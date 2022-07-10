import os
from .databases import ProblemsDatabase

CWD = os.getcwd()

statements_folder = os.path.join(CWD, "website", "problems", "statements")


def add_problems_to_database():
    db = ProblemsDatabase("problems.db")
    db.create_table()
    prbid = 0
    problem = {"id": 0, "name": "", "body": ""}
    problems = []
    commands = ["title", "body"]

    for problem_file_name in os.listdir(statements_folder):
        with open(os.path.join(statements_folder, problem_file_name), "r") as f:
            lines = f.readlines()
            onbody = False
            f.seek(0)
            for line in range(len(lines)):
                if lines[line].startswith("#"):
                    if (command := lines[line][1:].replace("\n", "")) == "title":
                        problem["name"] = lines[line + 1].replace("\n", "")
                        problem["id"] = prbid
                        prbid += 1
                    elif command == "body":
                        onbody = True
                        break
            if onbody:
                for line in range(line + 1, len(lines)):
                    problem["body"] += lines[line]
                problems.append(problem)
                problem = {"id": 0, "name": "", "body": ""}
    for problem in problems:
        db.add_problem(
            problem["name"],
            problem["body"],
            os.path.join(
                CWD,
                "website",
                "problems",
                "tests",
            ),
            os.path.join(
                CWD,
                "website",
                "problems",
                "answers",
            ),
        )
    db.close_connection()
