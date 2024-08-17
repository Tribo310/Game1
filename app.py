from tkinter import *
from PIL import Image, ImageTk
from BackEnd import bttn, switch_window, level_window,GameData

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
    bttn( welcome_window,850, 500, 'images/setting_btn.png', 'images/settings_hover_btn.png', lambda: switch_window(welcome_window,settingGui))
    bttn( welcome_window,850, 600, 'images/quit_btn.png', 'images/quit_hover_btn.png', lambda: welcome_window.destroy())

    welcome_window.mainloop()

def choice_level():

    choice_level = Tk()
    width_value = choice_level.winfo_screenwidth()
    height_value = choice_level.winfo_screenheight()
    choice_level.geometry("%dx%d+0+0" % (width_value, height_value))
    choice_level.title("Crossword Game")

    bg = Image.open('images/Welcome_img.png')
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
    
def settingGui():
    settingGui = Tk()
    settingGui.title("Options")
    width_value = settingGui.winfo_screenwidth()
    height_value = settingGui.winfo_screenheight()
    settingGui.geometry("%dx%d+0+0" % (width_value, height_value))
    
    bg = Image.open('images/background.png')
    resized_image = bg.resize((width_value, height_value), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)

    background_label = Label(settingGui, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    bttn(settingGui,100,900, 'images/back_btn.png', 'images/back_hover_btn.png',lambda: switch_window(settingGui,start_welcome_window))

    settingGui.mainloop()

start_welcome_window()