from functions.get_files_info import get_files_info

case_1_result = get_files_info("calculator", ".")
case_2_result = get_files_info("calculator", "pkg")
case_3_result = get_files_info("calculator", "/bin")
case_4_result = get_files_info("calculator", "../")

print(f"Result for current directory: {case_1_result}")
print(f"Result for 'pkg' directory: {case_2_result}")
print(f"Result for '/bin' directory: {case_3_result}")
print(f"Result for '../' directory: {case_4_result}")
