import tkinter as tk
import Login_Page as lp
import Recommend_page as rcmp
import Rating_page as rp
import Search_page as  sp
from Search_page import Search_page
import placeholder

class App_Recom(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
 # rcmp.Recommend_page,
        for F in (lp.Login_Page, rp.Rating_page,rcmp.Recommend_page, sp.Search_page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg="#E2EDFE") 

        self.show_frame("Login_Page")

    def show_frame(self, page_name, *args):
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "Recommend_page":
            frame.get_data(*args)
        if page_name == "Search_page":
            # frame.get_data(*args)
            frame.show_movie_1(*args)
        if page_name == "Rating_page":
            frame.create_movie_infor(*args)




if __name__ == "__main__":
    app = App_Recom()
    app.geometry("1200x750")
    app.title("A Movie Recommender System")
    app.mainloop()
    # window = tk.Tk()
    
    