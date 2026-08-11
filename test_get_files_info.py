from functions.get_files_info import get_files_info

case_1_result = get_files_info("calculator", ".")
case_2_result = get_files_info("calculator", "/bin")
case_3_result = get_files_info("calculator", "../")
case_4_result = get_files_info("calculator", "main.py")

print(f"Result for '.': {case_1_result}")
print(f"Result for '/bin': {case_2_result}")
print(f"Result for '../': {case_3_result}")
print(f"Result for 'main.py': {case_4_result}")
