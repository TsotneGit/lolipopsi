import subprocess
import os
import subprocess
from .databases import ProblemsDatabase

CWD = os.getcwd()


def test_solution(prbid, code):
    prbid = str(int(prbid) - 1)
    db = ProblemsDatabase("problems.db")
    problem = db.get_problem(str(int(prbid) + 1))
    db.close_connection()
    test_folder = problem[3]
    answer_folder = problem[4]
    test_file = os.path.join(CWD, test_folder, f"prb{prbid}")
    answer_file = os.path.join(CWD, answer_folder, f"prb{prbid}")

    with open(os.path.join(test_folder, test_file), "r") as f:
        tests = "".join(f.readlines()).split("#")

    with open(os.path.join(answer_folder, answer_file), "r") as f:
        answers = "".join(f.readlines()).split("#")

    answers.pop(0)
    tests.pop(0)
    answers.pop(-1)
    tests.pop(-1)

    for test, answer in zip(tests, answers):
        if test.startswith("\n"):
            test = test[1:]
        if answer.startswith("\n"):
            answer = answer[1:]

        with open(
            os.path.join(CWD, "website", "problems", "temp", "temp.py"), "w"
        ) as f:
            f.write(code)
        with open(os.path.join(CWD, "website", "problems", "temp", "test"), "w") as f:
            f.write(test)
        try:
            output = subprocess.check_output(
                [
                    "py",
                    os.path.join(CWD, "website", "problems", "temp", "temp.py"),
                ],
                stdin=open(
                    os.path.join(CWD, "website", "problems", "temp", "test"), "r"
                ),
                universal_newlines=True,
            )
        except:
            raise Exception
        os.remove(os.path.join(CWD, "website", "problems", "temp", "test"))
        os.remove(os.path.join(CWD, "website", "problems", "temp", "temp.py"))
        # print(output)
        # print(answer)
        # print(test)
        # if output.endswith("\n"):
        #     output = output[:-1]
        # print(len(output))
        # print(len(answer))
        if output != answer:
            return False
    return True
