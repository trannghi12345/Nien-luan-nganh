import tkinter as tk
import placeholder
from PIL import Image, ImageTk
from tkinter import messagebox
import sql
import Recommend_page
class Login_Page(tk.Frame):
    # def get_data(self, entry):
    #     print(entry.get())
    conn = sql.connect()
    cursor = conn.cursor()
    data = 1

    def select_userpass(self, user_id):
        sql_select = f"SELECT password FROM users WHERE users_id = {user_id}"
        return self.cursor.execute(sql_select).fetchall()[0][0]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #Create frame
        frame = tk.Frame(self, width=1200, height=750, background="#E2EDFE")
        frame.pack(expand=True, fill=tk.BOTH)

        camera = tk.Canvas(frame, width=135, height=75, background="#E2EDFE", highlightthickness=0)
        camera.place(x=533, y=188)
        camera_photo = ImageTk.PhotoImage(Image.open("picture/camera.png").resize((134, 74)))
        camera.create_image(0, 0, image=camera_photo, anchor="nw")
        camera.image = camera_photo

        #Create form
        form = tk.Frame(frame, width=300, height=198, background="#E2EDFE")
        form.place(x=450, y=355)

        #Create username
        username = tk.Canvas(form, width=300, height=45, background="#E2EDFE", highlightthickness=0)
        username.place(x=0, y=0)
        username.create_rectangle(0, 0, 299, 44, outline="#213AC0")
        username_photo = ImageTk.PhotoImage(Image.open("picture/user.png").resize((18, 18)))
        username.create_image(15, 14, image=username_photo, anchor="nw")
        username.image = username_photo
        #Input username
        username_entry = placeholder.EntryWithPlaceholder(username, "Nhập mã người dùng", "#213AC0")
        username_entry.place(x=48, y=13)
        username_entry.configure(width=27, background="#E2EDFE", bd=0, font=("Montserrat", 12))


        #Create password
        password = tk.Canvas(form, width=300, height=45, background="#E2EDFE", highlightthickness=0)
        password.place(x=0, y=65)
        password.create_rectangle(0, 0, 299, 44, outline="#213AC0")
        password_photo = ImageTk.PhotoImage(Image.open("picture/lock.png").resize((18, 21)))
        password.create_image(15, 12, image=password_photo, anchor="nw")
        password.image = password_photo
        #Input password
        password_entry = placeholder.EntryWithPlaceholder(password, "Nhập mật khẩu", "#213AC0", 1)
        password_entry.place(x=48, y=13)
        password_entry.configure(width=27, background="#E2EDFE", bd=0, font=("Montserrat", 12))

        def show_home():
            username_entry_data = username_entry.get()
            self.controller.show_frame("Recommend_page", username_entry_data) 


        #Create button login
        login_btn = tk.Canvas(form, width=300, height=45, background="#E2EDFE", highlightthickness=0)
        login_btn.place(x=0, y=153)
        login_btn_photo = ImageTk.PhotoImage(Image.open("picture/button_1.jpg"))
        login_btn.create_image(0, 0, image=login_btn_photo)
        login_btn.image = login_btn_photo
        button_1 = tk.Button(
            login_btn,
            image=login_btn_photo,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: check_login(),
            relief="flat"
        )
        button_1.place(x=0, y=0)


        def check_login():
            username_entry_data = username_entry.get()
            if password_entry.get() != self.select_userpass(username_entry.get()):
                messagebox.showerror("Lỗi xác thực", "Nhập sai mã người dùng hoặc mật khẩu")
            else:
                controller.show_frame("Recommend_page", username_entry_data)
