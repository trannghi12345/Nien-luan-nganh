import tkinter as tk
from PIL import Image, ImageTk
import placeholder
from tkinter import messagebox
import sql

class Rating_page(tk.Frame):
    conn = sql.connect()
    cursor = conn.cursor()
    users_id = 1
    movie_id = 1
    movie=[]
    keyword = "the"


    def create_username(self, i):
       i_str = str(i)
       uname1 = tk.Label(self,text="Người dùng", font=("Montserrat", 14, "bold"), background="#E2EDFE")
       uname1.place(x=880, y=30)
       uname = tk.Label(self, text=str(i), font=("Montserrat", 14, "bold"), name="my_label",background="#E2EDFE")
       uname.place(x=1000, y=30)

    def select_movie(self, movie_id_i):
        global movie_id
        self.movie_id = movie_id_i
        movie_infor = []
        sql_select = f"select name, rating, total_time, image_path from movie where movie_id = {self.movie_id}"
        execute = self.cursor.execute(sql_select).fetchall()
        movie_infor.append([execute[0][0], execute[0][1], execute[0][2], execute[0][3]])
        return movie_infor
    def click_event_1(self):
        # label_del = self.nametowidget("my_label_1")
        # label_del.destroy()
        global keyword
        self.keyword = str(self.search_input.get())
        print(self.keyword)
        self.controller.show_frame("Search_page", self.users_id,0,self.keyword)


    def get_data(self,input_data, input_movie_id):
        global users_id
        global movie_id
        global movie
        self.movie =[]
        self.users_id = input_data
        self.movie_id = input_movie_id
        self.create_username(input_data)
        print(self.movie_id)
        # self.users_id = self.get_user_id()
        # self.movie_id = self.get_movie_id()
        self.movie = self.select_movie(self.movie_id)
        #self print(self.movie_id)
        # return self.users_id, self.movie_id
    def get_movie_id(self):
        return self.movie_id
    def get_user_id(self):
        return self.users_id


    def select_rating(self, users_id, movie_id):
        try:
            sql_select = f"select rating from rating where users_id = {users_id} and movie_id={movie_id}"
            return self.cursor.execute(sql_select).fetchall()[0][0]
        except:
            return 0

    def select_other_rating(self, users_id_i, movie_id_i):
        global users_id
        self.users_id = users_id_i
        global movie_id
        self.movie_id = movie_id_i
        sql_select = f"select rating, users_id from rating where movie_id={self.movie_id} and not users_id = {self.users_id}"
        number_movie = len(self.cursor.execute(sql_select).fetchall())
        result = []
        if number_movie <= 2:
            for i in range(number_movie):
                result.append([self.cursor.execute(sql_select).fetchall()[i][0],
                               self.cursor.execute(sql_select).fetchall()[i][1]])
            for i in range(number_movie, 3):
                result.append([0, 0])
        else:
            for i in range(3):
                result.append([self.cursor.execute(sql_select).fetchall()[i][0],
                               self.cursor.execute(sql_select).fetchall()[i][1]])
        return result

   

    def insert_update(self, users_id_i, movie_id_i, rating):
        global users_id
        self.users_id = users_id_i
        global movie_id
        self.movie_id = movie_id_i
        sql_select = f"SELECT rating FROM rating WHERE movie_id = {self.movie_id} AND users_id = {self.users_id}"
        sql_insert = f"INSERT INTO rating VALUES ({self.movie_id}, {self.users_id}, {rating})"
        sql_update = f"UPDATE rating SET rating = {rating} WHERE movie_id = {self.movie_id} AND users_id = {self.users_id}"
        if not self.cursor.execute(sql_select).fetchall():
            self.cursor.execute(sql_insert)
            self.conn.commit()
        else:
            self.cursor.execute(sql_update)
            self.conn.commit()

    def create_movie_infor(self,input_data, input_movie_id):
        global users_id
        global movie_id
        global movie
        self.movie =[]
        self.users_id = input_data
        self.movie_id = input_movie_id
        self.create_username(input_data)
        print(self.movie_id)
        # self.users_id = self.get_user_id()
        # self.movie_id = self.get_movie_id()
        self.movie = self.select_movie(self.movie_id)
        poster = tk.Canvas(self, width=367, height=555, highlightthickness=0)
        poster.place(x=30, y=119)
        poster_photo = ImageTk.PhotoImage(Image.open(f"{self.movie[0][3]}").resize((367, 555)))
        poster.create_image(0, 0, image=poster_photo, anchor="nw")
        poster.image = poster_photo

        movie_infor = tk.Canvas(self, width=706, height=120, highlightthickness=0, background="#E2EDFE")
        movie_infor.place(x=439, y=115)
        movie_infor.create_text(0, 1, text=f"{self.movie[0][0]}", font=("Montserrat", 48, "bold"), anchor="nw")

        movie_rating = tk.Canvas(movie_infor, width=88, height=42, highlightthickness=0, background="#E2EDFE")
        movie_rating.place(x=16, y=80)

        rating_star_photo = ImageTk.PhotoImage(Image.open("picture/yellow_star.png").resize((27, 27)))
        movie_rating.create_image(14, 7, image=rating_star_photo, anchor="nw")
        movie_rating.image = rating_star_photo
        movie_rating.create_text(45, 5, text=f"{self.movie[0][1]}", font=("Montserrat", 20, "bold"), anchor="nw")

        movie_time = tk.Canvas(movie_infor, width=88, height=42, highlightthickness=0, background="#E2EDFE")
        movie_time.place(x=141, y=78)

        time_photo = ImageTk.PhotoImage(Image.open("picture/clock.png").resize((35, 35)))
        movie_time.create_image(5, 5, image=time_photo, anchor="nw")
        movie_time.image = time_photo
        movie_time.create_text(40, 6, text=f"{self.movie[0][2]}", font=("Montserrat", 22, "bold"), anchor="nw")

        rating_movie = tk.Canvas(self, width=673, height=128, highlightthickness=0, background="#E2EDFE")
        rating_movie.place(x=439, y=235)

        rating_movie.create_text(7, 15, text="ĐÁNH GIÁ BỘ PHIM NÀY", font=("Montserrat", 30, "bold"), anchor="nw")
        rating_movie_photo = ImageTk.PhotoImage(Image.open("picture/white_star.png").resize((48, 48)))
        rating_movie_photo1 = ImageTk.PhotoImage(Image.open("picture/yellow_star.png").resize((48, 48)))
        rating_movie.image = rating_movie_photo

        global count
        def rated_movie(index):
            if index == 1:
                btn_star1.configure(image=rating_movie_photo1)
                btn_star2.configure(image=rating_movie_photo)
                btn_star3.configure(image=rating_movie_photo)
                btn_star4.configure(image=rating_movie_photo)
                btn_star5.configure(image=rating_movie_photo)
            if index == 2:
                btn_star1.configure(image=rating_movie_photo1)
                btn_star2.configure(image=rating_movie_photo1)
                btn_star3.configure(image=rating_movie_photo)
                btn_star4.configure(image=rating_movie_photo)
                btn_star5.configure(image=rating_movie_photo)
            if index == 3:
                btn_star1.configure(image=rating_movie_photo1)
                btn_star2.configure(image=rating_movie_photo1)
                btn_star3.configure(image=rating_movie_photo1)
                btn_star4.configure(image=rating_movie_photo)
                btn_star5.configure(image=rating_movie_photo)
            if index == 4:
                btn_star1.configure(image=rating_movie_photo1)
                btn_star2.configure(image=rating_movie_photo1)
                btn_star3.configure(image=rating_movie_photo1)
                btn_star4.configure(image=rating_movie_photo1)
                btn_star5.configure(image=rating_movie_photo)
            if index == 5:
                btn_star1.configure(image=rating_movie_photo1)
                btn_star2.configure(image=rating_movie_photo1)
                btn_star3.configure(image=rating_movie_photo1)
                btn_star4.configure(image=rating_movie_photo1)
                btn_star5.configure(image=rating_movie_photo1)
            global count
            count = index

        btn_star1 = tk.Button(rating_movie,
                              image=rating_movie_photo,
                              highlightthickness=0,
                              command=lambda: rated_movie(1),
                              relief="flat",
                              background="#E2EDFE", activebackground="#E2EDFE"
                              )
        btn_star1.place(x=7, y=65)
        btn_star2 = tk.Button(rating_movie,
                              image=rating_movie_photo,
                              highlightthickness=0,
                              command=lambda: rated_movie(2),
                              relief="flat",
                              background="#E2EDFE", activebackground="#E2EDFE"
                              )
        btn_star2.place(x=106, y=65)
        btn_star3 = tk.Button(rating_movie,
                              image=rating_movie_photo,
                              highlightthickness=0,
                              command=lambda: rated_movie(3),
                              relief="flat",
                              background="#E2EDFE", activebackground="#E2EDFE"
                              )
        btn_star3.place(x=205, y=65)
        btn_star4 = tk.Button(rating_movie,
                              image=rating_movie_photo,
                              highlightthickness=0,
                              command=lambda: rated_movie(4),
                              relief="flat",
                              background="#E2EDFE", activebackground="#E2EDFE"
                              )
        btn_star4.place(x=304, y=65)
        btn_star5 = tk.Button(rating_movie,
                              image=rating_movie_photo,
                              highlightthickness=0,
                              command=lambda: rated_movie(5),
                              relief="flat",
                              background="#E2EDFE", activebackground="#E2EDFE"
                              )
        btn_star5.place(x=403, y=65)

        send_photo = ImageTk.PhotoImage(Image.open("picture/send.png").resize((48, 48)))
        rating_movie.image = send_photo
        rated_movie(self.select_rating(self.users_id, self.movie_id))

        def send_db():
            messagebox.showinfo("Xác nhận", "Đánh giá phim thành công")
            self.insert_update(self.users_id, self.movie_id, count)

        btn_send = tk.Button(rating_movie,
                             image=send_photo,
                             highlightthickness=0,
                             command=lambda: send_db(),
                             relief="flat",
                             background="#E2EDFE", activebackground="#E2EDFE"
                             )
        btn_send.place(x=502, y=65)

        other_rating = tk.Canvas(self, width=683, height=354, highlightthickness=0, background="#E2EDFE")
        other_rating.place(x=439, y=368)
        other_rating.create_text(8, 16, text="ĐIỂM ĐÁNH GIÁ CỦA NGƯỜI DÙNG KHÁC", font=("Montserrat", 20, "bold"), anchor="nw")

        other_rating_photo = ImageTk.PhotoImage(Image.open("picture/white_star.png").resize((18 ,18)))
        other_rating_photo1 = ImageTk.PhotoImage(Image.open("picture/yellow_star.png").resize((18, 18)))
        other_rating.image = other_rating_photo

        other1 = self.select_other_rating(self.users_id, self.movie_id)[0][1]
        other_rating1 = tk.Canvas(other_rating, width=261, height=70, highlightthickness=0, background="#FAF2F2")
        other_rating1.place(x=8, y=48)
        other_rating1.create_image(9, 13, image=self.avatar, anchor="nw")
        other_rating1.create_text(56, 12, text=f"Người dùng {other1}", font=("Montserrat", 15, "bold"), anchor="nw")
        other_rating1.image = other_rating_photo1

        user1_rated = self.select_other_rating(self.users_id, self.movie_id)[0][0]
        if user1_rated == 0:
            other_rating1.destroy()
        else:
            for i in range(user1_rated):
                other_rating1.create_image(55 + (i * 18), 38, image=other_rating_photo1, anchor="nw")
            for i in range(user1_rated, 5):
                other_rating1.create_image(55 + (i * 18), 38, image=other_rating_photo, anchor="nw")

        other2 = self.select_other_rating(self.users_id, self.movie_id)[1][1]
        other_rating2 = tk.Canvas(other_rating, width=261, height=70, highlightthickness=0, background="#FAF2F2")
        other_rating2.place(x=8, y=142)
        other_rating2.create_image(9, 13, image=self.avatar, anchor="nw")
        other_rating2.create_text(56, 12, text=f"Người dùng {other2}", font=("Montserrat", 15, "bold"), anchor="nw")

        user2_rated = self.select_other_rating(self.users_id, self.movie_id)[1][0]
        if user2_rated == 0:
            other_rating2.destroy()
        else:
            for i in range(user2_rated):
                other_rating2.create_image(55 + (i * 18), 38, image=other_rating_photo1, anchor="nw")
            for i in range(user2_rated, 5):
                other_rating2.create_image(55 + (i * 18), 38, image=other_rating_photo, anchor="nw")

        other3 = self.select_other_rating(self.users_id, self.movie_id)[2][1]
        other_rating3 = tk.Canvas(other_rating, width=261, height=70, highlightthickness=0, background="#FAF2F2")
        other_rating3.place(x=8, y=236)
        other_rating3.create_image(9, 13, image=self.avatar, anchor="nw")
        other_rating3.create_text(56, 12, text=f"Người dùng {other3}", font=("Montserrat", 15, "bold"), anchor="nw")

        user3_rated = self.select_other_rating(self.users_id, self.movie_id)[2][0]
        if user3_rated == 0:
            other_rating3.destroy()
        else:
            for i in range(user3_rated):
                other_rating3.create_image(55 + (i * 18), 38, image=other_rating_photo1, anchor="nw")
            for i in range(user3_rated, 5):
                other_rating3.create_image(55 + (i * 18), 38, image=other_rating_photo, anchor="nw")

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        # global movie
        self.controller = controller
        # self.movie = self.select_movie(self.movie_id)
        frame = tk.Frame(self, width=1200, height=750, background="#E2EDFE")
        frame.pack(expand=True, fill=tk.BOTH)

        frame_search = tk.Frame(frame, width=508, height=48)
        frame_search.place(x=30, y=20)

        search = tk.Canvas(frame_search, width=508, height=48, background="#E2EDFE", highlightthickness=0)
        search.place(x=0, y=0)

        home_photo = ImageTk.PhotoImage(Image.open("picture/home.png").resize((43, 37)))
        search.image = home_photo

        btn_home = tk.Button(search,
                             image=home_photo,
                             borderwidth=0,
                             highlightthickness=0,
                             command=lambda: controller.show_frame("Recommend_page", self.users_id),
                             relief="flat",
                             background="#E2EDFE", activebackground="#E2EDFE"
                             )
        btn_home.place(x=6, y=7)

        search.create_rectangle(58, 0, 478, 47, fill="#FFFFFF", outline="#FFFFFF")
        self.search_input = placeholder.EntryWithPlaceholder(search, "Nhập tên phim", "#213AC0")
        self.search_input.place(x=70, y=13)
        self.search_input.configure(width=30, background="#FFFFFF", bd=0, font=("Montserrat", 14))

        glass = tk.Canvas(search, width=45, height=45, background="#FFFFFF", highlightthickness=0)
        glass.place(x=435, y=4)
        glass_photo = ImageTk.PhotoImage(Image.open("picture/glass.png").resize((39, 38)))
        glass.image = glass_photo

        btn_glass = tk.Button(glass,
                              image=glass_photo,
                              borderwidth=0,
                              highlightthickness=0,
                              command=lambda: self.click_event_1(),
                              relief="flat",
                              background="#FFFFFF", activebackground="#FFFFFF"
                              )
        btn_glass.place(x=0, y=0)

        frame_user = tk.Frame(frame, width=268, height=48)
        frame_user.place(x=902, y=20)
        user = tk.Canvas(frame_user, width=268, height=48, highlightthickness=0, background="#E2EDFE")
        user.place(x=0, y=0)

        # user.create_text(12, 14, text=f"Người dùng {users_id}", font=("Montserrat", 14, "bold"), anchor="nw")
        self.avatar = ImageTk.PhotoImage(Image.open("picture/avatar.png").resize((42, 40)))
        user.create_image(165, 6, image=self.avatar, anchor="nw")
        user.image = self.avatar

        log_out = tk.Canvas(user, width=48, height=43, highlightthickness=0, background="#E2EDFE")
        log_out.place(x=220, y=2)
        log_out_photo = ImageTk.PhotoImage(Image.open("picture/log_out.png").resize((48, 43)))
        log_out.create_image(3, 0, image=log_out_photo, anchor="nw")
        log_out.image = log_out_photo

        btn_log_out = tk.Button(log_out,
                                image=log_out_photo,
                                highlightthickness=0,
                                command=lambda: check_logout(),
                                relief="flat",
                                background="#E2EDFE", activebackground="#E2EDFE"
                                )
        btn_log_out.place(x=0, y=0)

        def check_logout():
            ask = messagebox.askokcancel("Xác nhận", "Bạn có muốn đăng xuất?")
            if ask is True:
                self.controller.show_frame("Login_Page")

