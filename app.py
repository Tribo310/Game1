from tkinter import *
from PIL import Image, ImageTk
from BackEnd import bttn, switch_window, level_window,GameData
from tkinter import ttk
import sqlite3
# Ganaa
print("Hello")
def start_welcome_window():
    welcome_window = Tk()
    width_value = welcome_window.winfo_screenwidth()
    height_value = welcome_window.winfo_screenheight()
    welcome_window.geometry("%dx%d+0+0" % (width_value, height_value))
    welcome_window.title("Crossword Game")

    # Background image
    bg = Image.open('images/Welcome_img.png')
    resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)

    background_label = Label(welcome_window, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a menu label without explicitly setting a background
    bttn( welcome_window,850, 400, 'images/start_btn.png', 'images/start_hover_btn.png', lambda: switch_window(welcome_window,choice_level))
    bttn( welcome_window,850, 500, 'images/rank_btn.png', 'images/rank_hover_btn.png', lambda: switch_window(welcome_window,rank_gui))
    bttn( welcome_window,850, 600, 'images/quit_btn.png', 'images/quit_hover_btn.png', lambda: welcome_window.destroy())

    welcome_window.mainloop()

def choice_level():

    choice_level = Tk()
    width_value = choice_level.winfo_screenwidth()
    height_value = choice_level.winfo_screenheight()
    choice_level.geometry("%dx%d+0+0" % (width_value, height_value))
    choice_level.title("Crossword Game")

    bg = Image.open('images/background.png')
    resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    background_label = Label(choice_level, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    bttn( choice_level,850, 400, 'images/level1_btn.png', 'images/level1_hover_btn.png', lambda: switch_window(choice_level, lambda: level_window(GameData[0])))
    bttn( choice_level,850, 500, 'images/level2_btn.png', 'images/level2_hover_btn.png', lambda: switch_window(choice_level, lambda: level_window(GameData[1])))
    bttn( choice_level,850, 600, 'images/level3_btn.png', 'images/level3_hover_btn.png', lambda: switch_window(choice_level, lambda: level_window(GameData[2])))

    img_a = ImageTk.PhotoImage(Image.open('images/Back_btn.png'))
    bttn(choice_level,100,900, 'images/back_btn.png', 'images/back_hover_btn.png',lambda: switch_window(choice_level,start_welcome_window))
    choice_level.mainloop()
class Database:
    def __init__(self, game_time):
        self.master = Toplevel()  # Use the passed master instance
        self.game_time = game_time  # Store the passed game_time as an instance variable
        self.master.title("Database")
        self.master.geometry("320x320")

        bg = Image.open('images/background2.png')
        resized_image = bg.resize((320, 320), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)  # Store bg_image as an instance variable
        background_label = Label(self.master, image=self.bg_image)  # Use self.bg_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_table()

        # Entry for name
        self.f_name = Entry(self.master, width=30)
        self.f_name.grid(row=0, column=1, padx=10, pady=10)

        # Label for name
        self.f_name_label = Label(self.master, text="First Name")
        self.f_name_label.grid(row=0, column=0, padx=10, pady=10)

        # Submit button
        self.add_btn = Button(self.master, text='Submit', command=self.submit)
        self.add_btn.grid(row=3, column=0, pady=10, padx=10, ipadx=100, columnspan=2)

        # Show records button
        self.show_btn = Button(self.master, text="Show Records", command=self.query)
        self.show_btn.grid(row=4, column=0, pady=10, padx=10, ipadx=82, columnspan=2)

    def create_table(self):
        conn = sqlite3.connect('GameLevel1.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS addresses (
                    f_name TEXT,
                    game_score INTEGER
                    )''')
        conn.commit()
        conn.close()

    def submit(self):
        conn = sqlite3.connect('GameDataBase.db')
        c = conn.cursor()

        c.execute("INSERT INTO addresses (f_name, game_score) VALUES (:f_name, :game_score)",
                  {
                      'f_name': self.f_name.get(),
                      'game_score': self.game_time  # Use the instance variable game_time
                  })

        conn.commit()
        conn.close()

        # Clear the entry box after submission
        self.f_name.delete(0, END)

    def query(self):
        conn = sqlite3.connect('GameDataBase.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM addresses")
        records = c.fetchall()

        # Initialize the variable to store all records
        print_records = ""
        for record in records:
            print_records += str(record) + "\n"

        # Display the records in a Label
        query_label = Label(self.master, text=print_records)
        query_label.grid(row=5, column=0, columnspan=2)

        conn.commit()
        conn.close()

    