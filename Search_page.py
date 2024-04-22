import tkinter as tk
import placeholder
from PIL import Image, ImageTk
from tkinter import messagebox
import sql


class Search_page(tk.Frame):
    conn = sql.connect()
    cursor = conn.cursor()
    movie_infor = []
    users_id = 1
    movie_id = 1

    def search_movie(self, title):
        self.movie_infor = []
        try:
            sql_select = (f"SELECT movie_id, name, year, image_path FROM movie"
                          f" WHERE name LIKE '%{title}%' ORDER BY rating DESC")
            execute = self.cursor.execute(sql_select).fetchall()
            for i in range(self.count_movie(title)):
                self.movie_infor.append([execute[i][0], execute[i][1], execute[i][2], execute[i][3]])
            # print(self.movie_infor)
        except:
            return 0
    def create_username(self, i):
       i_str = str(i)
       frame_user = tk.Frame(self.frame, background="#E2EDFE")
       frame_user.rowconfigure(0, weight=1)
       frame_user.columnconfigure(0, weight=1)
       frame_user.grid_columnconfigure(0, minsize=600)
       frame_user.grid(row=0, column=1, sticky="nwse")
       user = tk.Canvas(frame_user, width=268, height=48, highlightthickness=0, background="#E2EDFE")
       user.grid(row=0, column=0, sticky="ne", padx=30, pady=20)
       user.create_text(12, 14, text=f"Người dùng {i_str}", font=("Montserrat", 14, "bold"), anchor="nw")
       avatar = ImageTk.PhotoImage(Image.open("picture/avatar.png").resize((42, 40)))
       user.create_image(165, 6, image=avatar, anchor="nw")
       user.image = avatar
       log_out = tk.Canvas(user, width=48, height=43, highlightthickness=0, background="#E2EDFE")
       log_out.place(x=220, y=2)
       log_out_photo = ImageTk.PhotoImage(Image.open("picture/log_out.png").resize((48, 43)))
       log_out.create_image(3, 0, image=log_out_photo, anchor="nw")
       log_out.image = log_out_photo
       btn_log_out = tk.Button(log_out,
                                image=log_out_photo,
                                highlightthickness=0,
                                command=lambda: self.check_logout(),
                                relief="flat",
                                background="#E2EDFE", activebackground="#E2EDFE"
                                )
       btn_log_out.place(x=0, y=0)


    def count_movie(self, title):
        if title != "":
            sql_count = f"SELECT COUNT(*) FROM movie WHERE name LIKE '%{title}%'"
            return int(self.cursor.execute(sql_count).fetchall()[0][0])
        else:
            return 0

    def check_logout(self):
        ask = messagebox.askokcancel("Xác nhận", "Bạn có muốn đăng xuất?")
        if ask is True:
            self.controller.show_frame("Login_Page")

    def find_frame_con(self, frame_cha, name):
        for child in frame_cha.winfo_children():
            if isinstance(child, tk.Frame) and child.winfo_name() == name:
                return 1
            return 0
    def click_event(self,input_movie_id):
        global movie_id
        self.movie_id = input_movie_id
        self.controller.show_frame("Rating_page", self.users_id, self.movie_id)

    def create_movie(self, index, frame_main):
        movie = tk.Canvas(frame_main, height=163, highlightthickness=0, background="#FAF2F2")
        movie.grid(row=index, column=0, padx=30, pady=10, columnspan=2, sticky="nsew")
        movie_poster = ImageTk.PhotoImage(Image.open(f"{self.movie_infor[index][3]}").resize((109, 163)))
        movie.create_rectangle(0, 0, 1400, 163, width=0, tags="mv")
        movie.create_image(0, 0, image=movie_poster, anchor="nw", tags="mv")
        movie.image = movie_poster
        movie.create_text(120, 30, text=f"{self.movie_infor[index][1]}",
                          font=("Montserrat", 30, "bold"), anchor="nw", tags="mv")
        movie.create_text(120, 80, text=f"{self.movie_infor[index][2]}",
                          font=("Montserrat", 30, "bold"), anchor="nw", tags="mv")
        movie.tag_bind("mv", "<Button-1>", lambda event: self.click_event(self.movie_infor[index][0]))

    def show_movie_1(self,input_data, count, input_data_search):
        global users_id
        self.users_id = input_data
        self.create_username(input_data)
        
        self.search_movie(str(input_data_search))
        print(input_data_search)

        def update_scrollregion():
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if self.find_frame_con(self.frame, "my") == 1 and count == 0:
            frame_del = self.frame.nametowidget("my")
            frame_del.destroy()
        else:
            frame_main = tk.Frame(self.frame, name="my", background="#E2EDFE")
            frame_main.columnconfigure(0, weight=1)
            frame_main.rowconfigure(0, weight=1)
            frame_main.grid(row=1, column=0, columnspan=2, sticky="nsew")
            count_movie = self.count_movie(str(input_data_search))

            if count_movie - count*7 <= 7:
                for i in range(count_movie):
                    self.create_movie(i, frame_main)
                if count_movie > 3:
                    frame_back_to_top = tk.Frame(frame_main, background="#E2EDFE")
                    frame_back_to_top.columnconfigure(0, weight=1)
                    frame_back_to_top.rowconfigure(0, weight=1)
                    frame_back_to_top.grid(row=(count+1)*7, column=1, sticky="nsew")
                    btn_back_to_top = tk.Button(frame_back_to_top,
                                                image=self.back_to_top_photo,
                                                command=lambda: self.canvas.yview_moveto(0),
                                                relief="flat",
                                                background="#E2EDFE", activebackground="#E2EDFE")
                    btn_back_to_top.grid(sticky="ne", column=1, padx=30)
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            else:
                for i in range((count+1)*7):
                    self.create_movie(i, frame_main)
                frame_more_film = tk.Frame(frame_main, background="#E2EDFE")
                frame_more_film.columnconfigure(0, weight=1)
                frame_more_film.rowconfigure(0, weight=1)
                frame_more_film.grid(row=(count+1)*7, column=0, sticky="nsew")
                btn_more_film = tk.Button(frame_more_film, text="Xem thêm", command=lambda: self.show_movie_1(input_data,count,input_data_search),
                                          font=("Montserrat", 15, "bold"),
                                          relief="flat",
                                          background="#E2EDFE", activebackground="#E2EDFE",
                                          fg="#213AC0", activeforeground="#213AC0")
                btn_more_film.grid(sticky="nw", column=0, pady=5)

                frame_back_to_top = tk.Frame(frame_main, background="#E2EDFE")
                frame_back_to_top.columnconfigure(0, weight=1)
                frame_back_to_top.rowconfigure(0, weight=1)
                frame_back_to_top.grid(row=(count + 1) * 7, column=1, sticky="nsew")
                btn_back_to_top = tk.Button(frame_back_to_top,
                                            image=self.back_to_top_photo,
                                            command=lambda: self.canvas.yview_moveto(0),
                                            relief="flat",
                                            background="#E2EDFE", activebackground="#E2EDFE")
                btn_back_to_top.grid(sticky="ne", column=1, padx=30)
                count += 1
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_movie(self,input_data, count):
        global users_id
        self.users_id = input_data
        self.create_username(input_data)
        
        self.search_movie(str(self.search_input.get()))
        print(self.search_input.get())

        def update_scrollregion():
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if self.find_frame_con(self.frame, "my") == 1 and count == 0:
            frame_del = self.frame.nametowidget("my")
            frame_del.destroy()
        else:
            frame_main = tk.Frame(self.frame, name="my", background="#E2EDFE")
            frame_main.columnconfigure(0, weight=1)
            frame_main.rowconfigure(0, weight=1)
            frame_main.grid(row=1, column=0, columnspan=2, sticky="nsew")
            count_movie = self.count_movie(str(self.search_input.get()))

            if count_movie - count*7 <= 7:
                for i in range(count_movie):
                    self.create_movie(i, frame_main)
                if count_movie > 3:
                    frame_back_to_top = tk.Frame(frame_main, background="#E2EDFE")
                    frame_back_to_top.columnconfigure(0, weight=1)
                    frame_back_to_top.rowconfigure(0, weight=1)
                    frame_back_to_top.grid(row=(count+1)*7, column=1, sticky="nsew")
                    btn_back_to_top = tk.Button(frame_back_to_top,
                                                image=self.back_to_top_photo,
                                                command=lambda: self.canvas.yview_moveto(0),
                                                relief="flat",
                                                background="#E2EDFE", activebackground="#E2EDFE")
                    btn_back_to_top.grid(sticky="ne", column=1, padx=30)
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            else:
                for i in range((count+1)*7):
                    self.create_movie(i, frame_main)
                frame_more_film = tk.Frame(frame_main, background="#E2EDFE")
                frame_more_film.columnconfigure(0, weight=1)
                frame_more_film.rowconfigure(0, weight=1)
                frame_more_film.grid(row=(count+1)*7, column=0, sticky="nsew")
                btn_more_film = tk.Button(frame_more_film, text="Xem thêm", command=lambda: self.show_movie(input_data,count),
                                          font=("Montserrat", 15, "bold"),
                                          relief="flat",
                                          background="#E2EDFE", activebackground="#E2EDFE",
                                          fg="#213AC0", activeforeground="#213AC0")
                btn_more_film.grid(sticky="nw", column=0, pady=5)

                frame_back_to_top = tk.Frame(frame_main, background="#E2EDFE")
                frame_back_to_top.columnconfigure(0, weight=1)
                frame_back_to_top.rowconfigure(0, weight=1)
                frame_back_to_top.grid(row=(count + 1) * 7, column=1, sticky="nsew")
                btn_back_to_top = tk.Button(frame_back_to_top,
                                            image=self.back_to_top_photo,
                                            command=lambda: self.canvas.yview_moveto(0),
                                            relief="flat",
                                            background="#E2EDFE", activebackground="#E2EDFE")
                btn_back_to_top.grid(sticky="ne", column=1, padx=30)
                count += 1
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self, highlightthickness=0, yscrollcommand=scrollbar.set, background="#E2EDFE")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas, background="#E2EDFE", width=1200, height=750)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.back_to_top_photo = ImageTk.PhotoImage(Image.open("picture/back_to_top.png").resize((45, 45)))


        # Create search
        self.frame_search = tk.Frame(self.frame, background="#E2EDFE")
        self.frame_search.rowconfigure(0, weight=1)
        self.frame_search.columnconfigure(0, weight=1)
        self.frame_search.grid_columnconfigure(0, minsize=600)
        self.frame_search.grid(sticky="nwse")

        self.search = tk.Canvas(self.frame_search, width=508, height=48, background="#E2EDFE", highlightthickness=0)
        self.search.grid(sticky="nw", padx=30, pady=20)

        home_photo = ImageTk.PhotoImage(Image.open("picture/home.png").resize((43, 37)))
        self.search.image = home_photo

        btn_home = tk.Button(self.search,
                             image=home_photo,
                             borderwidth=0,
                             highlightthickness=0,
                             command=lambda: controller.show_frame("Recommend_page", self.users_id),
                             relief="flat",
                             background="#E2EDFE", activebackground="#E2EDFE"
                             )
        btn_home.place(x=6, y=7)

        self.search.create_rectangle(58, 0, 478, 47, fill="#FFFFFF", outline="#FFFFFF")
        self.search_input = placeholder.EntryWithPlaceholder(self.search, "Nhập tên phim", "#213AC0")
        self.search_input.place(x=70, y=13)
        self.search_input.configure(width=30, background="#FFFFFF", bd=0, font=("Montserrat", 14))

        glass = tk.Canvas(self.search, width=45, height=45, background="#FFFFFF", highlightthickness=0)
        glass.place(x=435, y=4)
        glass_photo = ImageTk.PhotoImage(Image.open("picture/glass.png").resize((39, 38)))
        glass.image = glass_photo

        btn_glass = tk.Button(glass,
                              image=glass_photo,
                              borderwidth=0,
                              highlightthickness=0,
                              command=lambda: self.show_movie(self.users_id, 0),
                              relief="flat",
                              background="#FFFFFF", activebackground="#FFFFFF"
                              )
        btn_glass.place(x=0, y=0)

        frame_user = tk.Frame(self.frame, background="#E2EDFE")
        frame_user.rowconfigure(0, weight=1)
        frame_user.columnconfigure(0, weight=1)
        frame_user.grid_columnconfigure(0, minsize=600)
        frame_user.grid(row=0, column=1, sticky="nwse")
        user = tk.Canvas(frame_user, width=268, height=48, highlightthickness=0, background="#E2EDFE")
        user.grid(row=0, column=0, sticky="ne", padx=30, pady=20)


        log_out = tk.Canvas(user, width=48, height=43, highlightthickness=0, background="#E2EDFE")
        log_out.place(x=220, y=2)
        log_out_photo = ImageTk.PhotoImage(Image.open("picture/log_out.png").resize((48, 43)))
        log_out.create_image(3, 0, image=log_out_photo, anchor="nw")
        log_out.image = log_out_photo

        btn_log_out = tk.Button(log_out,
                                image=log_out_photo,
                                highlightthickness=0,
                                command=lambda: self.check_logout(),
                                relief="flat",
                                background="#E2EDFE", activebackground="#E2EDFE"
                                )
        btn_log_out.place(x=0, y=0)




