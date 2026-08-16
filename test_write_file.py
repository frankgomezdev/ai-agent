from functions.write_file import write_file

test_result_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
test_result_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
test_result_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

print(test_result_1)
print(test_result_2)
print(test_result_3)