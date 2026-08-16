from functions.get_file_content import get_file_content

test_result_1 = get_file_content("calculator", "lorem.txt")
test_result_2 = get_file_content("calculator", "main.py")
test_result_3 = get_file_content("calculator", "pkg/calculator.py")
test_result_4 = get_file_content("calculator", "/bin/cat") 
test_result_5 = get_file_content("calculator", "pkg/does_not_exist.py")

print(f"lorem.txt length: {len(test_result_1)}")
print(f"lorem.txt truncated: {'truncated' in test_result_1}")

print(test_result_2)
print(test_result_3)
print(test_result_4)
print(test_result_5)
