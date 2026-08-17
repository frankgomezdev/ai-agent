from functions.run_python_file import run_python_file

test_result_1 = run_python_file("calculator", "main.py") 
test_result_2 = run_python_file("calculator", "main.py", ["3 + 5"])
test_result_3 = run_python_file("calculator", "tests.py")
test_result_4 = run_python_file("calculator", "../main.py")
test_result_5 = run_python_file("calculator", "nonexistent.py") 
test_result_6 = run_python_file("calculator", "lorem.txt")

print(test_result_1)
print(test_result_2)
print(test_result_3)
print(test_result_4)
print(test_result_5)
print(test_result_6)