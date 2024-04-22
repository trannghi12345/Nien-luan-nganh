from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Canvas
import pandas as pd

import back as bk
import sql



r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

ratings_base = pd.read_csv('ml-100k/ub.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')

rate_train = ratings_base.values
rate_test = ratings_test.values

#indices start from 0
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

current_index = 4
current_coor_idx = 0
coordinates_list=[[38,400], [274,400], [510,400], [746,400], [982,400]]
pic_list=[]
movie_name_list=[]
rating_list=[]
total_time_list=[]
year_list=[]



def create_rectangle(x,y,a,b,**options):
   if 'alpha' in options:
      # Calculate the alpha transparency for every color(RGB)
      alpha = int(options.pop('alpha') * 255)
      # Use the fill variable to fill the shape with transparent color
      fill = options.pop('fill')
      fill = window.winfo_rgb(fill) + (alpha,)
      image = Image.new('RGBA', (a-x, b-y), fill)
      images.append(ImageTk.PhotoImage(image))
      canvas.create_image(x, y, image=images[-1], anchor='nw')
      canvas.create_rectangle(x, y,a,b, **options)

def create_canvas(x1, y1, cw, ch):
   rcanvas = Canvas(window, width=cw, height=ch, background="#F5F5F5")
   rcanvas.place(x=x1, y=y1)
   return rcanvas

def resize_picture(w,h,image):
   resize_image = image.resize((w,h), Image.LANCZOS)
   i_image = ImageTk.PhotoImage(resize_image)
   return i_image


def create_recomendation(x_canvas,y_canvas,cw,ch,image,Movie_Name,avg_rate,total_time,year):
   rcanvas = create_canvas(x_canvas,y_canvas,cw,ch)
   i_image = resize_picture(180,250,image)
   rcanvas.create_image(rcanvas_width // 2, 0, anchor="n", image=i_image)

   rcanvas.create_text(rcanvas_width // 2, 260, text=Movie_Name, font=("Arial", 12), fill="black", width="160", justify="center", anchor="n")

   avg_star = Image.open("star.png")
   avg_star_image = resize_picture(15,15,avg_star)
   rcanvas.create_image(10, 310, anchor="n", image=avg_star_image)
   rcanvas.create_text(32,320,text=avg_rate,font=("Arial",12),fill="black")

   clock = Image.open("clock.png")
   clock_image = resize_picture(20,20,clock)
   rcanvas.create_image(62,310, anchor="n",image=clock_image)
   rcanvas.create_text(102,320, text=total_time+" phút",font=("Arial",12),fill="black")
   rcanvas.create_text(158,320, text=year,font=("Arial",12),fill="black")
   return rcanvas, i_image, avg_star_image, clock_image

def show_next_canvas():
   global current_index
   global current_coor_idx
   global left_index
   if left_index < 4 and left_index >= 1:
      for i in range(5):
         current_index = (current_index + 1)
         if current_index in [0,5,10,15]:
            current_coor_idx = 0
         elif current_index in [1,6,11,16]:
            current_coor_idx = 1
         elif current_index in [2,7,12,17]:
            current_coor_idx = 2
         elif current_index in [3,8, 13, 18]:
            current_coor_idx = 3
         else:
            current_coor_idx = 4
         rcanvas, i_image, avg_star_image, clock_image = create_recomendation(coordinates_list[current_coor_idx][0],
         coordinates_list[current_coor_idx][1],
         rcanvas_width,rcanvas_height,
         pic_list[current_index],
         movie_name_list[current_index],
         rating_list[current_index],
         total_time_list[current_index],
         year_list[current_index])
         images.append(i_image)
         images.append(avg_star_image)
         images.append(clock_image)
         print(current_index)
      left_index = left_index + 1
      # print(left_index)
      return rcanvas, i_image, avg_star_image, clock_image

def show_previous_canvas():
   global current_index
   current_index = current_index - 4
   global current_coor_idx
   global left_index
   if left_index <= 4 and left_index > 1:
      for i in range(5):
         current_index = (current_index - 1)
         if current_index in [0,5,10,15]:
            current_coor_idx = 0
         elif current_index in [1,6,11,16]:
            current_coor_idx = 1
         elif current_index in [2,7,12,17]:
            current_coor_idx = 2
         elif current_index in [3,8, 13, 18]:
            current_coor_idx = 3
         else:
            current_coor_idx = 4
         rcanvas, i_image, avg_star_image, clock_image = create_recomendation(coordinates_list[current_coor_idx][0],
         coordinates_list[current_coor_idx][1],
         rcanvas_width,rcanvas_height,
         pic_list[current_index],
         movie_name_list[current_index],
         rating_list[current_index],
         total_time_list[current_index],
         year_list[current_index])
         images.append(i_image)
         images.append(avg_star_image)
         images.append(clock_image)
         # print(current_index)
      current_index = current_index + 4
      left_index = left_index - 1
      # print(left_index)
      return rcanvas, i_image, avg_star_image, clock_image

def create_username(i):
   i_str = str(i)
   uname = tk.Label(text=str(i), font=("Arial", 12), name="my_label")
   uname.place(x=1080, y=30)

def get_data():
   global array_items
   global movie_name_list
   global year_list
   global rating_list
   global total_time_list
   global pic_list
   movie_name_list = []
   year_list = []
   rating_list = []
   total_time_list = []
   pic_list = []
   array_items = []
   label_del = window.nametowidget("my_label")
   label_del.destroy()
   global left_index
   left_index = 1
   global current_index
   current_index = 4 
   global data
   data = entry.get()
   # if (data.match("\d")):
   create_username(data)
   recommended_items = []
   recommended_items = rs.print_recommendation(data)
   cursor = sql.connect()

   for i in range(len(recommended_items)):
      sql_select = sql.select(recommended_items[i])
      x = cursor.execute(sql_select)
      a = x.fetchall()
      array_items.append(a)
   for i in range(len(array_items)):
      movie_name_list.append(array_items[i][0][1])
      year_list.append(str(array_items[i][0][2]))
      rating_list.append(str(array_items[i][0][3]))
      total_time_list.append(str(array_items[i][0][4]))
      pic_list.append(Image.open(str(array_items[i][0][5])))
   for i in range(5):
      rcanvas, i_image, avg_star_image, clock_image = create_recomendation(coordinates_list[i][0],coordinates_list[i][1],rcanvas_width,rcanvas_height,pic_list[i],movie_name_list[i],
      rating_list[i],total_time_list[i],year_list[i])
      images.append(i_image)
      images.append(avg_star_image)
      images.append(clock_image)
   print(movie_name_list,year_list,total_time_list,pic_list)
   npage = tk.Label(text=str(left_index)+"/"+str(right_index), font=("Arial", 12),)
   npage.place(x=1000, y=370)
   return rcanvas, i_image, avg_star_image, clock_image
   return data


array_items = []


def get_data_1(event):
   global array_items
   global movie_name_list
   global year_list
   global rating_list
   global total_time_list
   global pic_list
   movie_name_list = []
   year_list = []
   rating_list = []
   total_time_list = []
   pic_list = []
   array_items = []
   label_del = window.nametowidget("my_label")
   label_del.destroy()
   global left_index
   left_index = 1
   global current_index
   current_index = 4 
   global data
   data = entry.get()
   # if (data.match("\d")):
   create_username(data)
   recommended_items = []
   recommended_items = rs.print_recommendation(data)
   cursor = sql.connect()

   for i in range(len(recommended_items)):
      sql_select = sql.select(recommended_items[i])
      x = cursor.execute(sql_select)
      a = x.fetchall()
      print(a)
      array_items.append(a)

   for i in range(len(array_items)):
      movie_name_list.append(array_items[i][0][1])
      year_list.append(str(array_items[i][0][2]))
      rating_list.append(str(array_items[i][0][3]))
      total_time_list.append(str(array_items[i][0][4]))
      pic_list.append(Image.open(str(array_items[i][0][5])))
   for i in range(5):
      rcanvas, i_image, avg_star_image, clock_image = create_recomendation(coordinates_list[i][0],coordinates_list[i][1],rcanvas_width,rcanvas_height,pic_list[i],movie_name_list[i],
      rating_list[i],total_time_list[i],year_list[i])
      images.append(i_image)
      images.append(avg_star_image)
      images.append(clock_image)
   print(movie_name_list,year_list,total_time_list)
   npage = tk.Label(text=str(left_index)+"/"+str(right_index), font=("Arial", 12),)
   npage.place(x=1000, y=370)
   return rcanvas, i_image, avg_star_image, clock_image
   return data

#chisotrang
def page_index():
   global left_index
   if left_index <= 4 and left_index >= 1:
      npage = tk.Label(text=str(left_index)+"/"+str(right_index), font=("Arial", 12))
      npage.place(x=1000, y=370)



# Tạo cửa sổ chính
window = tk.Tk()
window.title("A Movie Recommender System")
window.geometry("1200x750")


label = tk.Label(text="Vui lòng nhập vào mã người dùng:", font=("Arial", 12))
entry = tk.Entry(width=10)
#Nhan OK
button = tk.Button(window, text="Ok", command=lambda: get_data())
entry.place(x=290, y=30)
# Nhan enter
entry.bind("<Return>",get_data_1)
# entry.bind("<Return>", print_recommendation_1)
# entry.bind("<Return>", lambda event: get_data_1() and print_recommendation_1())

uname = tk.Label(text="Người dùng", font=("Arial", 12))
uname.place(x=990, y=30)
uname1 = tk.Label(text="?", font=("Arial", 12), name="my_label")
uname1.place(x=1080, y=30)
uimg = Image.open("user.png")
resized_img = uimg.resize((50, 50), Image.LANCZOS)
image = ImageTk.PhotoImage(resized_img)
ulabel = tk.Label(window, image=image)
label.place(x=38, y=30)
button.place(x=370, y=30)
ulabel.place(x=1112, y=10)


#Banner
bimg = Image.open("BG.png")
resized_bimg = bimg.resize((1144, 275), Image.LANCZOS)
bimage = ImageTk.PhotoImage(resized_bimg)
#Icon 
icon = Image.open("camera.png")
resized_icon = icon.resize((100,100), Image.LANCZOS)
icon_image = ImageTk.PhotoImage(resized_icon)
#Canvas Banner
canvas_width = bimage.width()
canvas_height = bimage.height()
canvas = create_canvas(28, 80, canvas_width, canvas_height)
canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=bimage)  # Or image_scaled
rect_width = bimage.width()
rect_height = bimage.height()
create_rectangle(0, 0,rect_width,rect_height, fill="black", alpha=.9)
canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=icon_image)  # Or image_scaled
canvas.create_text(canvas_width // 2, 200, text="Có thể bạn sẽ thích!", font=("Arial", 20), fill="white")


#Navigation
button1 = tk.Button(window, text="<",command=lambda: [show_previous_canvas(), page_index()])
button1.place(x=1050, y=370)
button2 = tk.Button(window, text=">",command=lambda: [show_next_canvas(), page_index()])
button2.place(x=1070, y=370)


#chisotrang
npage = tk.Label(text=str(left_index)+"/"+str(right_index), font=("Arial", 12),)
npage.place(x=1000, y=370)


#Khu vực nhập dữ liệu




# Khởi động vòng lặp sự kiện
window.mainloop()


