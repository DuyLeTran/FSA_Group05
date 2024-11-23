import os

def delete_ds_store(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == ".DS_Store":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

# Đường dẫn tới thư mục bạn muốn xử lý
directory_path = "/Users/tranleduy/FPT_AI_Project/6_OJT202/FSA_Group05"

# Gọi hàm để xóa file
delete_ds_store(directory_path)