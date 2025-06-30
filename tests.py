from functions.run_python import run_python_file

def run_tests():
    print("\nTest 1: run main.py")
    print(run_python_file("calculator", "main.py"))

    print("\nTest 2: run tests.py")
    print(run_python_file("calculator", "tests.py"))

    print("\nTest 3: run ../main.py (should error)")
    print(run_python_file("calculator", "../main.py"))

    print("\nTest 4: run nonexistent.py (should error)")
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    run_tests()
