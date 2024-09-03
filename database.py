from tkinter import *
from PIL import Image, ImageTk
import sqlite3

class BaseLevel:
    def __init__(self, level_name, game_time, db_name):
        self.master = Toplevel()
        self.level_name = level_name
        self.game_time = game_time
        self.db_name = db_name
        self.master.title(self.level_name)
        self.master.geometry("320x320")

        # Background image
        bg = Image.open('images/background2.png')
        resized_image = bg.resize((320, 320), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        background_label = Label(self.master, image=self.bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_table()

        # UI elements
        self.create_widgets()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS addresses (
                    f_name TEXT,
                    game_score INTEGER
                    )''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Entry for name
        self.f_name = Entry(self.master, width=30)
        self.f_name.grid(row=0, column=1, padx=10, pady=10)

        # Label for name
        f_name_label = Label(self.master, text="First Name")
        f_name_label.grid(row=0, column=0, padx=10, pady=10)

        # Submit button
        add_btn = Button(self.master, text='Submit', command=self.submit)
        add_btn.grid(row=3, column=0, pady=10, padx=10, ipadx=100, columnspan=2)

        # Show records button
        # show_btn = Button(self.master, text="Show Records", command=self.query)
        # show_btn.grid(row=4, column=0, pady=10, padx=10, ipadx=82, columnspan=2)

    def submit(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("INSERT INTO addresses (f_name, game_score) VALUES (:f_name, :game_score)",
                  {
                      'f_name': self.f_name.get(),
                      'game_score': self.game_time
                  })

        conn.commit()
        conn.close()

        # Clear the entry box after submission
        self.f_name.delete(0, END)

    def query(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("SELECT *, oid FROM addresses")
        records = c.fetchall()

        print_records = "\n".join([str(record) for record in records])

        # Display the records in a Label
        query_label = Label(self.master, text=print_records)
        query_label.grid(row=5, column=0, columnspan=2)

        conn.commit()
        conn.close()

class Level1(BaseLevel):
    def __init__(self, game_time):
        super().__init__("Level 1", game_time, 'GameLevel1.db')

class Level2(BaseLevel):
    def __init__(self, game_time):
        super().__init__("Level 2", game_time, 'GameLevel2.db')
class Level3(BaseLevel):
    def __init__(self, game_time):
        super().__init__("Level 2", game_time, 'GameLevel3.db')


if __name__ == "__main__":
    root = Tk()
    game_time1 = 50
    game_time2 = 35
    game_time3 = 48
    Level1(game_time1)

    root.mainloop()
