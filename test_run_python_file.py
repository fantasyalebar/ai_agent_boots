from functions.run_python_file import run_python_file

print("--- Test 1: Calculatrice (Usage) ---")
print(run_python_file("calculator", "main.py"))

print("\n--- Test 2: Calculatrice (Addition) ---")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print(run_python_file("calculator", "tests.py"))

print(run_python_file("calculator", "../main.py"))

print(run_python_file("calculator", "nonexistent.py"))

print(run_python_file("calculator", "lorem.txt"))


