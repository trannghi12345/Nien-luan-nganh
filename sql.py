import pyodbc

# Tạo kết nối với cơ sở dữ liệu SQL Server
def connect():
    conn = pyodbc.connect(
        "Driver=ODBC Driver 17 for SQL Server;"
        r"Server=LAPTOP-M7JP18Q0\SQLEXPRESS;"
        "Database=Recommend_Movies;"
        "Trusted_Connection=Yes;"
    )

    return conn



def select(mv_id):
    sql_select = f"SELECT * FROM movie WHERE movie_id = {mv_id}"  # Use f-string for safer interpolation
    return sql_select

