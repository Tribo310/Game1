from tkinter import Tk, Label, Entry, Button, Canvas, Toplevel, messagebox, Text, Frame, END, ttk
from PIL import Image, ImageTk
from tkinter.font import Font
from crossword_data import GameData
import time
import sqlite3

level_num = 0
play_time = 0

def switch_window(current_window, next_window_func):
    current_window.destroy()
    next_window_func()

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



def bttn(parent, x, y, image_path, hover_image_path, command):
    # Load images
    try:
        default_image = Image.open(image_path)
        default_photo = ImageTk.PhotoImage(default_image)
        hover_image = Image.open(hover_image_path)
        hover_photo = ImageTk.PhotoImage(hover_image)
    except Exception as e:
        print(f"Error loading button images: {e}")
        return

    button = Button(parent, image=default_photo, command=command, borderwidth=0)
    button.image = default_photo  # Keep a reference to avoid garbage collection
    button.place(x=x, y=y)

    def on_enter(event):
        button.config(image=hover_photo)
        button.image = hover_photo

    def on_leave(event):
        button.config(image=default_photo)
        button.image = default_photo

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    return button
class Gamedata:
    def __init__(self, parent, db_name):
        self.db_name = db_name

        # Ensure the table exists
        self.ensure_table_exists()

        # Clear existing content in the parent frame
        for widget in parent.winfo_children():
            widget.destroy()

        frame = Frame(parent)
        frame.pack()

        table = ttk.Treeview(frame, columns=('№', 'name', 'score'), show='headings')
        table.heading('№', text='Rank')
        table.heading('name', text='Name')
        table.heading('score', text="Score")
        table.pack(pady=20)  # Pack the table with padding

        # Database connection
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT f_name, game_score FROM addresses ORDER BY game_score ASC")  # Sort by score in ascending order
        records = c.fetchall()

        # Insert records into the table
        for i, record in enumerate(records, start=1):  # Enumerate to add a ranking number
            table.insert('', 'end', values=(i, record[0], record[1]))  # Insert each record with its ranking number

        conn.close()

    def ensure_table_exists(self):
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Create the table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS addresses (
                     id INTEGER PRIMARY KEY,
                     f_name TEXT NOT NULL,
                     game_score INTEGER NOT NULL)''')
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
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

class Stopwatch(Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._start_time = None
        self._elapsed_time = 0
        self._running = False
        self.config(text="00:00:00", font=('Arial', 20))

    def start(self):
        if not self._running:
            self._start_time = time.time() - self._elapsed_time
            self._running = True
            self._update()

    def stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsed_time = time.time() - self._start_time
            self._running = False

    def reset(self):
        if self._running:
            self.after_cancel(self._timer)
        self._start_time = time.time()
        self._elapsed_time = 0
        self.config(text="00:00:00")

    def _update(self):
        self._elapsed_time = time.time() - self._start_time
        self.config(text=self._format_time(self._elapsed_time))
        self._timer = self.after(50, self._update)

    def _format_time(self, elapsed_time):
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

class CrosswordGame:
    def __init__(self, canvas, crossword_data, level_win):
        self.canvas = canvas
        self.correct_data = crossword_data[0]
        self.index_data = crossword_data[1]
        self.explanation_data = crossword_data[2]
        self.clues = crossword_data[3]
        self.level_win = level_win
        self.cells = {}
        self.entries = []
        self.create_grid()
        self.create_ui()
        self.stopwatch = Stopwatch(self.level_win, text="00:00:00")
        self.stopwatch.place(x=900, y=160)  # Adjust the position as needed
        self.start_stopwatch()

        self.play_time = 0

    def start_stopwatch(self):
        self.stopwatch.start()

    def create_grid(self):
        vcmd = (self.canvas.register(self.validate_input), '%P', '%W')

        for i, (row, col) in enumerate(self.index_data):
            entry = Entry(self.canvas, width=2, font=('Arial', 20), justify='center', validate='key', validatecommand=vcmd, bg='#fff')
            entry.grid(row=row, column=col, padx=0, pady=0)
            self.cells[(row, col)] = entry
            self.entries.append(entry)

        for (row, col), text in self.clues.items():
            if text:
                label = Label(self.canvas, text=text, font=('Arial', 12))
                label.grid(row=row, column=col, padx=0, pady=0)

    def validate_input(self, P, widget_name):
        if len(P) <= 1:
            if len(P) == 1:
                self.move_to_next_widget(widget_name)
            return True
        return False

    def move_to_next_widget(self, widget_name):
        current_widget = self.canvas.nametowidget(widget_name)
        if current_widget in self.entries:
            current_index = self.entries.index(current_widget)
            if current_index + 1 < len(self.entries):
                self.entries[current_index + 1].focus_set()

    def create_ui(self):
        bttn(self.level_win, 100, 900, 'images/back_btn.png', 'images/back_hover_btn.png', lambda: switch_window(self.level_win, choice_level))
        bttn(self.level_win, 600, 900, 'images/clear_btn.png', 'images/clear_hover_btn.png', self.clear_button)
        bttn(self.level_win, 1000, 900, 'images/submit_btn.png', 'images/submit_hover_btn.png', self.submit_button)
        bttn(self.level_win, 1600, 900, 'images/quit.png', 'images/quit_hover.png', self.level_win.destroy)

    def clear_button(self):
        for cell in self.cells.values():
            cell.delete(0, 'end')
            cell.config(bg='white')

    def submit_button(self, event=None):
        all_correct = True

        for i, (row, col) in enumerate(self.index_data):
            entry = self.cells[(row, col)]
            user_input = entry.get().lower()
            if user_input == self.correct_data[i]:
                entry.config(bg='#00ff00')
            else:
                entry.config(bg='red')
                all_correct = False

        if all_correct:
            global level_num
            global play_time

            self.stopwatch.stop()  # Stop the stopwatch to capture the current level time
            play_time += self.stopwatch._elapsed_time  # Accumulate the play time

            formatted_play_time = self.stopwatch._format_time(play_time)  # Format play time as a string
            Database(formatted_play_time)

            # if answer == 'yes':
            #     level_num += 1
            #     if level_num < len(GameData):
            #         switch_window(self.level_win, lambda: level_window(GameData[level_num]))
            #     else:
            #         messagebox.showinfo("End", f"You have completed all levels!\nYour total play time: {formatted_play_time}")
            #         self.level_win.destroy()  # Close the game window
            # else:
            #     self.level_win.destroy()  # Close the game window if the user doesn't want to proceed
            #     start_welcome_window()

    def move_cursor(self, row_delta, col_delta):
        current_widget = self.canvas.focus_get()
        if current_widget in self.entries:
            current_index = self.entries.index(current_widget)
            current_row, current_col = list(self.cells.keys())[current_index]

            new_row = current_row + row_delta
            new_col = current_col + col_delta

            if (new_row, new_col) in self.cells:
                self.cells[(new_row, new_col)].focus_set()

    def cursor_up(self, event):
        self.move_cursor(-1, 0)

    def cursor_down(self, event):
        self.move_cursor(1, 0)

    def cursor_left(self, event):
        self.move_cursor(0, -1)

    def cursor_right(self, event):
        self.move_cursor(0, 1)

    def cursor_move(self, event):
        self.move_cursor(0, -1)

def level_window(crossword_data):
    level_win = Tk()
    level_win.title(crossword_data[4])

    width_value = level_win.winfo_screenwidth()
    height_value = level_win.winfo_screenheight()
    level_win.geometry(f"{width_value}x{height_value}+0+0")

    try:
        bg = Image.open('images/background.png')
        resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return

    background_label = Label(level_win, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = Frame(level_win, bg='#00ffff')
    frame.pack(padx=350, pady=200, fill='both', expand=True)

    canvas = Canvas(frame, bg='#D9D9D9')
    canvas.pack(side='left', padx=10, pady=10, fill='both', expand=True)

    text_data = crossword_data[2]
    explanation_text = Text(frame, wrap='word', font=('Arial', 12))
    explanation_text.insert('end', text_data)
    explanation_text.pack(side='right', padx=10, pady=10, fill='both', expand=True)

    game = CrosswordGame(canvas, crossword_data, level_win)

    level_win.bind('<Up>', game.cursor_up)
    level_win.bind('<Down>', game.cursor_down)
    level_win.bind('<Left>', game.cursor_left)
    level_win.bind('<Right>', game.cursor_right)
    level_win.bind('<BackSpace>', game.cursor_move)
    level_win.bind('<Return>', game.submit_button)
    
 
    level_win.mainloop()

def rank_gui():
    root = Tk()
    root.title("Overview Rank")
    width_value = root.winfo_screenwidth()
    height_value = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (width_value, height_value))
    
    # Background image
    bg = Image.open('images/background.png')
    resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)

    background_label = Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Prevent image from being garbage collected
    root.bg_image = bg_image

    # Create a frame for the table and buttons
    frame = Frame(root, bg='#F72585')
    frame.pack(padx=700, pady=350, fill='both', expand=True)

    # Instantiate Gamedata with the first level by default
    Gamedata(frame, 'Gamelevel1.db')

    def update_gamedata(db_name):
        # Update the Gamedata instance with the selected level
        Gamedata(frame, db_name)

    # Example buttons
    bttn(root, 659, 100, 'images/1level.png', 'images/1hover_level.png', lambda: update_gamedata('Gamelevel1.db'))
    bttn(root, 860, 100, 'images/2level.png', 'images/2hover_level.png', lambda: update_gamedata('Gamelevel2.db'))
    bttn(root, 1061, 100, 'images/3level.png', 'images/3hover_level.png', lambda: update_gamedata('Gamelevel3.db'))
    bttn(root, 100, 900, 'images/back_btn.png', 'images/back_hover_btn.png', lambda: print("back"))

    root.mainloop()

# Test function call (replace GameData with your actual crossword data)
# level_window(GameData[0])
start_welcome_window()
