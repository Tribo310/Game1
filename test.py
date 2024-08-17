from tkinter import Tk, Label, Entry, Button, Canvas, Toplevel, messagebox, Text, Frame
from PIL import Image, ImageTk
from tkinter.font import Font
from crossword_data import GameData
import time

def switch_window(current_window, next_window_func):
    current_window.destroy()
    next_window_func()

def start_welcome_window():
    welcome_window = Tk()
    width_value = welcome_window.winfo_screenwidth()
    height_value = welcome_window.winfo_screenheight()
    welcome_window.geometry(f"{width_value}x{height_value}+0+0")
    welcome_window.title("Crossword Game")

    # Background image
    try:
        bg = Image.open('images/Welcome_img.png')
        resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return

    background_label = Label(welcome_window, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    bttn(welcome_window, 850, 400, 'images/start_btn.png', 'images/start_hover_btn.png', lambda: switch_window(welcome_window, open_choice_level_window))
    bttn(welcome_window, 850, 500, 'images/setting_btn.png', 'images/settings_hover_btn.png', lambda: switch_window(welcome_window, open_setting_window))
    bttn(welcome_window, 850, 600, 'images/quit_btn.png', 'images/quit_hover_btn.png', lambda: welcome_window.destroy())

    welcome_window.mainloop()

def open_choice_level_window():
    choice_window = Tk()
    width_value = choice_window.winfo_screenwidth()
    height_value = choice_window.winfo_screenheight()
    choice_window.geometry(f"{width_value}x{height_value}+0+0")
    choice_window.title("Crossword Game")

    try:
        bg = Image.open('images/background.png')
        resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return

    background_label = Label(choice_window, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    bttn(choice_window, 850, 400, 'images/level1_btn.png', 'images/level1_hover_btn.png', lambda: switch_window(choice_window, lambda: level_window(GameData[0])))
    bttn(choice_window, 850, 500, 'images/level2_btn.png', 'images/level2_hover_btn.png', lambda: switch_window(choice_window, lambda: level_window(GameData[1])))
    bttn(choice_window, 850, 600, 'images/level3_btn.png', 'images/level3_hover_btn.png', lambda: switch_window(choice_window, lambda: level_window(GameData[2])))

    img_a = ImageTk.PhotoImage(Image.open('images/Back_btn.png'))
    bttn(choice_window, 100, 900, 'images/back_btn.png', 'images/back_hover_btn.png', lambda: switch_window(choice_window, start_welcome_window))
    
    choice_window.mainloop()

def open_setting_window():
    setting_window = Tk()
    setting_window.title("Options")
    width_value = setting_window.winfo_screenwidth()
    height_value = setting_window.winfo_screenheight()
    setting_window.geometry(f"{width_value}x{height_value}+0+0")
    
    try:
        bg = Image.open('images/background.png')
        resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return

    background_label = Label(setting_window, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    bttn(setting_window, 100, 900, 'images/back_btn.png', 'images/back_hover_btn.png', lambda: switch_window(setting_window, start_welcome_window))
    
    setting_window.mainloop()

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
        bttn(self.level_win, 100, 900, 'images/back_btn.png', 'images/back_hover_btn.png', lambda: switch_window(self.level_win, open_choice_level_window))
        bttn(self.level_win, 850, 900, 'images/check.png', 'images/check_hover.png', self.submit_button)
        bttn(self.level_win, 1600, 900, 'images/quit.png', 'images/quit_hover.png', self.level_win.destroy)

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
            answer = messagebox.askquestion("Congratulations", "Next Level?")
            if answer == 'yes':
                global level_num
                level_num += 1
                if level_num >= len(GameData):
                    messagebox.showinfo("End", "You have completed all levels!")
                    self.level_win.destroy()
                else:
                    switch_window(self.canvas.winfo_toplevel(), lambda: level_window(GameData[level_num]))
            else:
                start_welcome_window()

    def move_cursor(self, row_delta, col_delta):
        current_widget = self.canvas.focus_get()
        if current_widget in self.entries:
            current_index = self.entries.index(current_widget)
            current_row, current_col = list(self.cells.keys())[current_index]
            
            # Debug: Print the current index and entry content
            print(f"Current Index: {current_index}, Entry Content: '{self.entries[current_index].get()}'")
            
            # Condition: Checking if the current entry is not empty
            if self.entries[current_index].get() != "":  # Replace with your actual condition
                print("Condition met: Moving Left")
                self.move_cursor(0, -1)  # Move left
            else:
                print("Condition not met: Moving Down")
                self.move_cursor(1, 0)  # Move down


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
 
    level_win.mainloop()

# Test function call (replace GameData with your actual crossword data)
level_window(GameData[0])
