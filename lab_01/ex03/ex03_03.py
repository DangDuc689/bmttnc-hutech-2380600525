def tao_tuple_tu_list(a):
    return tuple(a)
#Nhập danh sách số từ người dùng và xử lý chuỗi
input_list = input("Nhập danh sách số (phân tách bởi dấu phẩy): ")
numbers = list(map(int, input_list.split(',')))

my_tuple = tao_tuple_tu_list(numbers)
print("List", numbers)
print("Tuple từ list là:", my_tuple)