from functions.run_python import run_python_file


def test():
    print(run_python_file("calculator", "main.py"))
    print("")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))


if __name__ == "__main__":
    test()