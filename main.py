import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import threading
import subprocess

OPENED_FILE_PATH = ''
FONT_SIZE = 12
TAB_WIDTH = '1c'


# https://stackoverflow.com/questions/54395358/tkinter-runtimeerror-threads-can-only-be-started-once
class Task(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task, args=(master,))

        if not hasattr(master, 'thread_run') or not master.thread_run.is_alive():
            master.thread_run = self
            self.start()


# =====================================
# Menu bar functions
def run(master):
    code = master.editor.get('1.0', END)
    if not is_opened_file_set():
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code before running it')
        text.pack()
        return
    # TODO: Communicates to appear here what script is doing
    clear_code_output(master)
    command = f'kotlinc -script {OPENED_FILE_PATH}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    master.code_output.config(state=NORMAL)
    for c in iter(lambda: process.stdout.read(1), b''):

        master.code_output.insert(END, c)

    for c in iter(lambda: process.stderr.read(1), b''):
        master.code_output.insert(END, c)

    master.code_output.config(state=DISABLED)
    print("end of thread")
    # process.kill()
    # exit(0)


def clear_code_output(master):
    master.code_output.config(state=NORMAL)
    master.code_output.delete('1.0', END)
    master.code_output.config(state=DISABLED)


def update_currently_opened_file(path):
    global OPENED_FILE_PATH
    OPENED_FILE_PATH = path


def is_opened_file_set():
    global OPENED_FILE_PATH
    if OPENED_FILE_PATH == '':
        return False

    return True


# Opens file and sets global variable opened_file_path
def open_file(master):
    global OPENED_FILE_PATH
    try:
        path = askopenfilename(filetypes=[("Kotlin Files", "*.kts")])
    except FileNotFoundError:
        # TODO: alert it
        return

    if OPENED_FILE_PATH == path:
        return

    update_currently_opened_file(path)
    with open(path, 'r') as file:
        code = file.read()
        master.editor.delete('1.0', END)
        master.editor.insert('1.0', code)


# Behaviour depends on whether file is a new blank file or we edit existing saved file.
def save(master):
    if OPENED_FILE_PATH == '':
        save_as(master)
    else:
        do_save_code_to_path(OPENED_FILE_PATH, master)


# File browser pops up.
def save_as(master):
    try:
        path = asksaveasfilename(defaultextension=".kts", filetypes=[("Kotlin Files", "*.kts")])
        do_save_code_to_path(path, master)
        update_currently_opened_file(path)
    except FileNotFoundError as e:
        print(e.__repr__())
        # TODO: alert error


# Auxiliary function
def do_save_code_to_path(path, master):
    with open(path, 'w') as file:
        code = master.editor.get('1.0', END)
        file.write(code)


# Settings: font, font size, background color, font color...
def settings():
    print("Not implemented settings")


# New blank project. Possible extension to cascade 2 options: blank project and from template
def new_file():
    print("Not implemented new_file")


# =====================================
# The whole GUI declaration
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title('AppCode Student Test Task')
        # compiler.attributes("-fullscreen", True)
        self.geometry("1200x720")
        # compiler.resizable(False, False)

        # Menu bar at the top
        self.menu_bar = Menu(self)

        # File button
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', command=new_file)
        self.file_menu.add_command(label='Open', command=lambda: open_file(self))
        self.file_menu.add_command(label='Save', command=lambda: save(self))
        self.file_menu.add_command(label='Save As', command=lambda: save_as(self))
        self.file_menu.add_command(label='Exit', command=exit)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Status bar
        self.status = Label(self, height=1, text="Ready    ", bd=2, relief=FLAT, anchor=E)
        self.status.pack(side=BOTTOM, fill=X)

        # Run code button
        self.run_bar = Menu(self.menu_bar, tearoff=0)
        self.run_bar.add_command(label='Run', command=lambda: Task(self, run))
        self.menu_bar.add_cascade(label='Run', menu=self.run_bar)

        # Code output pane
        self.code_output = Text()
        self.code_output.config(state=DISABLED, bg='#2B2B2B', fg='#F7F7F7', font=("Courier", FONT_SIZE), height=10)
        self.code_output.pack(side=BOTTOM, fill=X)

        # Editor Pane with scroll bar
        self.editor_pane_scrollbar = tkinter.Scrollbar(self)
        self.editor = Text(bg='#3C3F41', fg='#F7F7F7', font=("Courier", FONT_SIZE), height=100, width=120,
                           insertbackground='white', undo=True, yscrollcommand=self.editor_pane_scrollbar.set)

        self.editor_pane_scrollbar.config(command=self.editor.yview)
        self.editor_pane_scrollbar.pack(side=RIGHT, fill=Y)
        self.editor.pack(side=TOP, fill=X, expand=True)

        scrollb = tkinter.Scrollbar(self, command=self.editor.yview)
        self.editor['yscrollcommand'] = scrollb.set

        self.config(menu=self.menu_bar)


# main
if __name__ == "__main__":
    App().mainloop()
