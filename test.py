from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

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

# Run the GUI
rank_gui()
