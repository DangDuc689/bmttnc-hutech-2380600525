def dao_nguoc_list(lst):
    return lst[::-1]
#Nhập danh sách số từ người dùng
input_list = input("Nhập danh sách số (phân tách bởi dấu ,):")
number = list(map(int, input_list.split(',')))
#Đảo ngược danh sách số và in ra kết quả
list_dao_nguoc = dao_nguoc_list(number)
print("Danh sách sau khi đảo ngược là: ", list_dao_nguoc)