import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Canvas
import pandas as pd
import back as bk 
import sql
import placeholder
import Search_page as sp
from tkinter import messagebox

class Recommend_page(tk.Frame):
	images=[]
	r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
	ratings_base = pd.read_csv('ml-100k/ub.base', sep='\t', names=r_cols, encoding='latin-1')
	ratings_test = pd.read_csv('ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')
	rate_train = ratings_base.values
	rate_test = ratings_test.values
	rate_train[:, :2] -= 1
	rate_test[:, :2] -= 1
	rs = bk.CF(rate_test, k = 30, uuCF = 1)
	rs.fit()
	rating = pd.concat([ratings_base, ratings_test], axis=0)
	rate = rating.values
	avg = []
	images=[]

	rcanvas_width = 180
	rcanvas_height = 330


	data = 1
	left_index = 1
	right_index = 4
	movie_id = 1

	current_index = 4
	current_coor_idx = 0
	coordinates_list=[[38,400], [274,400], [510,400], [746,400], [982,400]]
	pic_list=[]
	movie_id_list=[]
	movie_name_list=[]
	rating_list=[]
	total_time_list=[]
	year_list=[]
	array_items = []

	keyword = "the"
	
	def click_event(self,input_movie_id):
		global movie_id
		self.movie_id = input_movie_id
		self.controller.show_frame("Rating_page", self.data, self.movie_id)
		# print(Movie_Name)
		# print(self.movie_id)

	def click_event_1(self):
		# label_del = self.nametowidget("my_label_1")
		# label_del.destroy()
		global keyword
		self.keyword = str(self.search_input.get())
		print(self.keyword)
		self.controller.show_frame("Search_page", self.data,0,self.keyword)
	

   
	
	def create_canvas(self,x1, y1, cw, ch):
	   rcanvas = Canvas(self, width=cw, height=ch)
	   rcanvas.place(x=x1, y=y1)
	   return rcanvas

	def resize_picture(self,w,h,image):
	   resize_image = image.resize((w,h), Image.LANCZOS)
	   i_image = ImageTk.PhotoImage(resize_image)
	   return i_image


	def create_recomendation(self, x_canvas,y_canvas,cw,ch,image,movie_id,Movie_Name,avg_rate,total_time,year):
	   rcanvas = self.create_canvas(x_canvas,y_canvas,cw,ch)
	   i_image = self.resize_picture(180,250,image)
	   rcanvas.create_image(self.rcanvas_width // 2, 0, anchor="n", image=i_image, tags="my_circle")
	   rcanvas.image1 = i_image
	   rcanvas.create_text(self.rcanvas_width // 2, 260, text=Movie_Name, font=("Arial", 12), fill="black", width="160", justify="center", anchor="n")

	   avg_star = Image.open("star.png")
	   avg_star_image = self.resize_picture(15,15,avg_star)
	   rcanvas.create_image(10, 310, anchor="n", image=avg_star_image)
	   rcanvas.image2 = avg_star_image
	   rcanvas.create_text(32,320,text=avg_rate,font=("Arial",12),fill="black")

	   clock = Image.open("clock.png")
	   clock_image = self.resize_picture(20,20,clock)
	   rcanvas.create_image(62,310, anchor="n",image=clock_image)
	   rcanvas.image3 = clock_image
	   rcanvas.create_text(102,320, text=total_time+" phút",font=("Arial",12),fill="black")
	   rcanvas.create_text(158,320, text=year,font=("Arial",12),fill="black")
	   # rcanvas.bind("<Button-1>", self.click_event(Movie_Name))
	   rcanvas.tag_bind("my_circle", "<Button-1>", lambda event: self.click_event(movie_id))
	   return rcanvas

	def show_next_canvas(self):
	   global current_index
	   global current_coor_idx
	   global left_index
	   if self.left_index < 4 and self.left_index >= 1:
	      for i in range(5):
	         self.current_index = (self.current_index + 1)
	         if self.current_index in [0,5,10,15]:
	            self.current_coor_idx = 0
	         elif self.current_index in [1,6,11,16]:
	            self.current_coor_idx = 1
	         elif self.current_index in [2,7,12,17]:
	            self.current_coor_idx = 2
	         elif self.current_index in [3,8, 13, 18]:
	            self.current_coor_idx = 3
	         else:
	            self.current_coor_idx = 4
	         rcanvas = self.create_recomendation(self.coordinates_list[self.current_coor_idx][0],
	         self.coordinates_list[self.current_coor_idx][1],
	         self.rcanvas_width,self.rcanvas_height,
	         self.pic_list[self.current_index],
	         self.movie_id_list[self.current_index],
	         self.movie_name_list[self.current_index],
	         self.rating_list[self.current_index],
	         self.total_time_list[self.current_index],
	         self.year_list[self.current_index])
	         # self.images.append(i_image)
	         # self.images.append(avg_star_image)
	         # self.images.append(clock_image)
	         # print(current_index)
	      self.left_index = self.left_index + 1
	      print(self.left_index)
	      return rcanvas

	def show_previous_canvas(self):
	   global current_index
	   self.current_index = self.current_index - 4
	   global current_coor_idx
	   global left_index
	   if self.left_index <= 4 and self.left_index > 1:
	      for i in range(5):
	         self.current_index = (self.current_index - 1)
	         if self.current_index in [0,5,10,15]:
	            self.current_coor_idx = 0
	         elif self.current_index in [1,6,11,16]:
	            self.current_coor_idx = 1
	         elif self.current_index in [2,7,12,17]:
	            self.current_coor_idx = 2
	         elif self.current_index in [3,8, 13, 18]:
	            self.current_coor_idx = 3
	         else:
	            self.current_coor_idx = 4
	         rcanvas = self.create_recomendation(self.coordinates_list[self.current_coor_idx][0],
	         self.coordinates_list[self.current_coor_idx][1],
	         self.rcanvas_width,self.rcanvas_height,
	         self.pic_list[self.current_index],
	         self.movie_id_list[self.current_index],
	         self.movie_name_list[self.current_index],
	         self.rating_list[self.current_index],
	         self.total_time_list[self.current_index],
	         self.year_list[self.current_index])
	         # self.images.append(i_image)
	         # self.images.append(avg_star_image)
	         # self.images.append(clock_image)
	         # print(current_index)
	      self.current_index = self.current_index + 4
	      self.left_index = self.left_index - 1
	      print(self.left_index)
	      return rcanvas

	def create_username(self, i):
	   i_str = str(i)
	   uname1 = tk.Label(self,text="Người dùng", font=("Montserrat", 14, "bold"), background="#E2EDFE")
	   uname1.place(x=880, y=30)
	   uname = tk.Label(self, text=str(i), font=("Montserrat", 14, "bold"), name="my_label",background="#E2EDFE")
	   uname.place(x=1000, y=30)



	def get_data(self, input_data):
	   global array_items
	   global movie_name_list
	   global year_list
	   global rating_list
	   global total_time_list
	   global pic_list
	   global movie_id_list
	   self.movie_id_list = []
	   self.movie_name_list = []
	   self.year_list = []
	   self.rating_list = []
	   self.total_time_list = []
	   self.pic_list = []
	   self.array_items = []
	   # label_del = self.nametowidget("my_label")
	   # label_del.destroy()
	   global left_index
	   self.left_index = 1
	   global current_index
	   self.current_index = 4
	   global data
	   # self.data = entry.get()
	   self.data = input_data
	   # if (data.match("\d")):
	   self.create_username(self.data)
	   recommended_items = []
	   recommended_items = self.rs.print_recommendation(self.data)
	   cursor = sql.connect()

	   for i in range(len(recommended_items)):
	      sql_select = sql.select(recommended_items[i])
	      x = cursor.execute(sql_select)
	      a = x.fetchall()
	      self.array_items.append(a)
	   for i in range(len(self.array_items)):
	   	  self.movie_id_list.append(self.array_items[i][0][0])
	   	  self.movie_name_list.append(self.array_items[i][0][1])
	   	  self.year_list.append(str(self.array_items[i][0][2]))
	   	  self.rating_list.append(str(self.array_items[i][0][3]))
	   	  self.total_time_list.append(str(self.array_items[i][0][4]))
	   	  self.pic_list.append(Image.open(str(self.array_items[i][0][5])))
	   for i in range(5):
	      rcanvas = self.create_recomendation(self.coordinates_list[i][0],self.coordinates_list[i][1],self.rcanvas_width,self.rcanvas_height,self.pic_list[i],self.movie_id_list[i],self.movie_name_list[i],
	      self.rating_list[i],self.total_time_list[i],self.year_list[i])
	      # self.images.append(i_image)
	      # self.images.append(avg_star_image)
	      # self.images.append(clock_image)
	   print(self.movie_id_list,self.movie_name_list,self.year_list,self.total_time_list)
	   npage = tk.Label(self,text=str(self.left_index)+"/"+str(self.right_index), font=("Arial", 12),name="my_label_1")
	   npage.place(x=1000, y=370)
	   return rcanvas
	   return data

	def page_index(self):
	   global left_index
	   if self.left_index <= 4 and self.left_index >= 1:
	      npage = tk.Label(self,text=str(self.left_index)+"/"+str(self.right_index), font=("Arial", 12),name="my_label_1")
	      npage.place(x=1000, y=370)

	def __init__(self, parent, controller, *args, **kwargs):
	    tk.Frame.__init__(self, parent)
	    self.controller = controller
	    rcanvas_width = 180
	    rcanvas_height = 330
	    data = 1
	    left_index = 1
	    right_index = 4
	    current_index = 4
	    current_coor_idx = 0
	    coordinates_list=[[38,400], [274,400], [510,400], [746,400], [982,400]]
	    pic_list=[]
	    movie_name_list=[]
	    rating_list=[]
	    total_time_list=[]
	    year_list=[]
	    obj_Search_page = sp.Search_page(parent=parent, controller=self.controller)
	    back_to_top_photo = ImageTk.PhotoImage(Image.open("picture/back_to_top.png").resize((45, 45)))


	 

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
                             command=lambda: controller.show_frame("Recommend_page", self.data),
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
	    		controller.show_frame("Login_Page")
            

	    def create_rectangle(x,y,a,b,**options):
		    if 'alpha' in options:
		      	# Calculate the alpha transparency for every color(RGB)
		      	alpha = int(options.pop('alpha') * 255)
		      	fill = options.pop('fill')
		      	fill = self.winfo_rgb(fill) + (alpha,)
		      	# Use the fill variable to fill the shape with transparent color
		      	image = Image.new('RGBA', (a-x, b-y), fill)
		      	self.images.append(ImageTk.PhotoImage(image))
		      	canvas.create_image(x, y, image=self.images[-1], anchor='nw')
		      	canvas.create_rectangle(x, y,a,b, **options)

	    #Banner
	    bimg = Image.open("BG.png")
	    resized_bimg = bimg.resize((1144, 275), Image.LANCZOS)
	    bimage = ImageTk.PhotoImage(resized_bimg)
	    #icon
	    icon = Image.open("camera.png")
	    resized_icon = icon.resize((100,100), Image.LANCZOS)
	    icon_image = ImageTk.PhotoImage(resized_icon)

	    #Cannvas Banner
	    canvas_width = bimage.width()
	    canvas_height = bimage.height()
	    canvas = self.create_canvas(28, 80, canvas_width, canvas_height)
	    canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=bimage)
	    canvas.image1 = bimage
	    rect_width = bimage.width()
	    rect_height = bimage.height()


	    create_rectangle(0, 0, rect_width, rect_height, fill="black", alpha=.9)
	    # self.create_rectangle(0, 0,rect_width,rect_height, fill="black", alpha=.9)
	    canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=icon_image)
	    canvas.image2 = icon_image
	    canvas.create_text(canvas_width // 2, 200, text="Có thể bạn sẽ thích!", font=("Arial", 20), fill="white")
	    
	    button1 = tk.Button(self, text="<", command=lambda: [self.show_previous_canvas(), self.page_index()])
	    button1.place(x=1050, y=370)
	    button2 = tk.Button(self, text=">",command=lambda: [self.show_next_canvas(), self.page_index()])
	    button2.place(x=1070, y=370)
	    #chisotrang
	    npage = tk.Label(self,text=str(self.left_index)+"/"+str(self.right_index), font=("Arial", 12), name="my_label_1")
	    npage.place(x=1000, y=370)


