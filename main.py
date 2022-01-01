from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

OPENED_FILE_PATH = ''


# =====================================
# Menu bar functions
def run():
    code = editor.get('1.0', END)
    if not is_opened_file_set():
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code before running it')
        text.pack()
        return
    command = f'python {OPENED_FILE_PATH}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0', error)


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
    path = askopenfilename(filetypes=[("Python Files", "*.py")])

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
        path = asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
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

# Run code button
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

# Editor Pane
editor = Text()
editor.pack()

# Code output pane
code_output = Text()
code_output.pack()

# Main
compiler.config(menu=menu_bar)
compiler.mainloop()
