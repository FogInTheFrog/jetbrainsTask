from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

OPENED_FILE_PATH = ''
FONT_SIZE = 12


# =====================================
# Menu bar functions
def run():
    code = editor.get('1.0', END)
    if not is_opened_file_set():
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code before running it')
        text.pack()
        return
    # TODO: Communicates to appear here what script is doing
    clear_code_output()
    command = f'kotlinc -script {OPENED_FILE_PATH}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    code_output.config(state=NORMAL)
    for c in iter(lambda: process.stdout.read(1), b''):

        code_output.insert(END, c)

    for c in iter(lambda: process.stderr.read(1), b''):
        code_output.insert(END, c)

    code_output.config(state=DISABLED)


def clear_code_output():
    code_output.config(state=NORMAL)
    code_output.delete('1.0', END)
    code_output.config(state=DISABLED)


def update_currently_opened_file(path):
    global OPENED_FILE_PATH
    OPENED_FILE_PATH = path


def is_opened_file_set():
    global OPENED_FILE_PATH
    if OPENED_FILE_PATH == '':
        return False

    return True


# Opens file and sets global variable opened_file_path
def open_file():
    global OPENED_FILE_PATH
    path = askopenfilename(filetypes=[("Kotlin Files", "*.kts")])

    if OPENED_FILE_PATH == path:
        return

    update_currently_opened_file(path)
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)


# Behaviour depends on whether file is a new blank file or we edit existing saved file.
def save():
    if OPENED_FILE_PATH == '':
        save_as()
    else:
        do_save_code_to_path(OPENED_FILE_PATH)


# File browser pops up.
def save_as():
    try:
        path = asksaveasfilename(defaultextension=".kts", filetypes=[("Kotlin Files", "*.kts")])
        do_save_code_to_path(path)
        update_currently_opened_file(path)
    except FileNotFoundError as e:
        print(e.__repr__())
        # TODO: alert error


# Auxiliary function
def do_save_code_to_path(path):
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)


# Settings: font, font size, background color, font color...
def settings():
    print("Not implemented settings")


# New blank project. Possible extension to cascade 2 options: blank project and from template
def new_file():
    print("Not implemented new_file")

# =====================================
# The whole GUI declaration
compiler = Tk()
compiler.title('AppCode Student Test Task')
# compiler.attributes("-fullscreen", True)
compiler.geometry("1200x720")
# compiler.resizable(False, False)

# Menu bar at the top
menu_bar = Menu(compiler)

# File button
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

# Status bar
status = Label(compiler, height=1, text="Ready    ", bd=2, relief=FLAT, anchor=E)
status.pack(side=BOTTOM, fill=X)

# Run code button
run_bar = Menu(menu_bar, tearoff=0)

from threading import Thread
run_bar.add_command(label='Run', command=Thread(target=run).start)
menu_bar.add_cascade(label='Run', menu=run_bar)

# Code output pane
code_output = Text()
code_output.config(state=DISABLED, bg='#2B2B2B', fg='#F7F7F7', font=("Courier", FONT_SIZE), height=10)
code_output.pack(side=BOTTOM, fill=X)

# Editor Pane
editor = Text(bg='#3C3F41', fg='#F7F7F7', font=("Courier", FONT_SIZE), height=100, width=120)
editor.pack(side=TOP, fill=X, expand=True)


# Main
compiler.config(menu=menu_bar)
compiler.mainloop()
