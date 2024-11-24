import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
connection = sqlite3.connect("db.sqlite3")

# Tạo con trỏ để thực hiện truy vấn
cursor = connection.cursor()

# Câu lệnh SQL để đổi tên cột
sql = """
ALTER TABLE achievement_performance 
RENAME COLUMN score TO average_score;
"""

try:
    # Thực thi truy vấn
    cursor.execute(sql)
    print("Column renamed successfully.")
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")
finally:
    # Đóng kết nối
    connection.commit()
    connection.close()