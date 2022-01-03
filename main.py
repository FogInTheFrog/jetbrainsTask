import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from kotlin_keywords import exact_keyword
import threading
import subprocess


# Function manages threads created to run code. Prevents code to be run twice at the same time.
# https://stackoverflow.com/questions/54395358/tkinter-runtimeerror-threads-can-only-be-started-once
class Task(threading.Thread):
    def __init__(self, master, task, clear_output_before_execution, before_run_message):
        threading.Thread.__init__(self, target=task, args=(master, clear_output_before_execution, before_run_message,))

        if not hasattr(master, 'thread_run') or not master.thread_run.is_alive():
            master.thread_run = self
            self.start()


# Function manages to run threads, only after previous run ends
class TaskToRunSimultaneously(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task, args=(master,))

        clear_output_pane(master)

        if not is_path_to_file_set(master):
            alert_user_to_save_code(master)

        elif not hasattr(master, 'thread_run_multiple_times') or not master.thread_run_multiple_times.is_alive():
            master.thread_run_multiple_times = self
            self.start()


# Window pops up informing user to save file
def alert_user_to_save_code(master):
    save_prompt = Toplevel(height=200, width=300)
    text = Label(save_prompt, text='Please save your code before running it', height=6, width=40)
    text.pack()
    update_status_bar(master, "Unable to run code...")


# Function runs code under chosen path in extra process. To prevent app freezing, this
# function should be called by a new thread.
def run(master, clear_output_before_execution, before_run_message):
    update_status_bar(master, "Compiling...")

    # If the file to run is not selected pop up window appears and function returns.
    if not is_path_to_file_set(master):
        alert_user_to_save_code(master)

    # Clear all the output from the previous run
    if clear_output_before_execution:
        clear_output_pane(master)

    update_status_bar(master, "Running...")

    # Create subprocess using Popen to run the script. Popen was selected instead of run
    # because we want to live print the output instead of to execute a command and wait
    # until it finishes.
    command = f'kotlinc -script {master.ENV_OPENED_FILE_PATH}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Print to output pane
    master.code_output.config(state=NORMAL)  # enable writing to output pane
    # Print starting message
    if before_run_message != '':
        master.code_output.insert(END, before_run_message)

    # Read standard output from pipe and live print it to output pane
    for c in iter(lambda: process.stdout.read(1), b''):
        master.code_output.insert(END, c)

    # Read error output from pipe and live print it to output pane
    for c in iter(lambda: process.stderr.read(1), b''):
        master.code_output.insert(END, c, 'error')

    master.code_output.config(state=DISABLED)  # disable writing to output pane

    # Print return code of the script to status bar
    return_code = process.poll()
    if return_code is None:
        return_code = 0
    update_status_bar(master, f"Script finished with exit code {return_code}")


def clear_output_pane(master):
    master.code_output.config(state=NORMAL)
    master.code_output.delete('1.0', END)
    master.code_output.config(state=DISABLED)


def fill_editor_pane(master, code):
    master.editor.insert('1.0', code)


def clear_editor_pane(master):
    master.editor.delete('1.0', END)


def update_currently_opened_file(path, master):
    master.ENV_OPENED_FILE_PATH = path


def is_path_to_file_set(master):
    return master.ENV_OPENED_FILE_PATH != ''


# Changes text, that appears in status bar at the bottom of our app window.
def update_status_bar(master, new_status: str):
    master.status['text'] = new_status + "    "


# Opens file and sets its path as code to run in our application. The editor pane
# is filled with new data and unsaved progress is permanently lost. The file browser
# window pops up and we can select the location of certain file.
def open_file(master):
    try:
        path = askopenfilename(filetypes=[("Kotlin Files", "*.kts")])
    except FileNotFoundError:
        update_status_bar(master, "No file opened")
        return

    if master.ENV_OPENED_FILE_PATH == path:
        return

    update_currently_opened_file(path, master)
    try:
        with open(path, 'r') as file:
            clear_editor_pane(master)
            code = file.read()
            fill_editor_pane(master, code)
    except FileNotFoundError:
        update_status_bar(master, "No file opened")
        return


# Allows user to save the content of editor pane to a file. Behaviour depends on
# whether file is a new blank file or we are editing existing saved file. In the first
# case we just update the file on the path in master. In the former case, the file browser
# window pops up and we can select the location where we want to save our file.
def save(master):
    if not is_path_to_file_set(master):
        return save_as(master)
    else:
        try:
            do_save_code_to_path(master.ENV_OPENED_FILE_PATH, master)
            return True
        except FileNotFoundError:
            return False


# Allows user to save the content of editor pane to a file. File browser pops up, so
# we can select the location where the content of the editor pane will be saved.
def save_as(master):
    try:
        path = asksaveasfilename(defaultextension=".kts", filetypes=[("Kotlin Files", "*.kts")])
        do_save_code_to_path(path, master)
        update_currently_opened_file(path, master)
        return True
    except FileNotFoundError as e:
        return False


# Auxiliary function to fill file under given path with the content of editor pane.
def do_save_code_to_path(path, master):
    with open(path, 'w') as file:
        code = master.editor.get('1.0', END)
        file.write(code)


# Settings: font, font size, background color, font color...
def settings():
    # TODO: to implement some day maybe
    print("Not implemented settings")


# Creates new blank project. Any unsaved changes will be permanently lost.
def new_file(master):
    master.ENV_OPENED_FILE_PATH = ''
    clear_editor_pane(master)


# Saves file and runs code
def save_and_run(master):
    if save(master):
        Task(master, run, True, "")


# Runs code multiple times
def run_multiple_times(master):
    popup_window = AskForNumberOfRunsWindow(master)
    master.wait_window(popup_window.top_window)

    try:
        number_of_times = int(popup_window.number_of_executions)
    except ValueError:
        update_status_bar(master, "You have to put Integer to input box...    ")
        return

    for i in range(number_of_times):
        Task(master, run, False, f"\nScript execution number: {i + 1}/{number_of_times}:\n\n")
        while master.thread_run.is_alive():
            master.thread_run.join(0.2)


# Runs code multiple times only if save was successful
def save_and_run_multiple_times(master):
    if save(master):
        TaskToRunSimultaneously(master, run_multiple_times)


# Performs highlighting of the code, should be called every t milliseconds to highlight keywords in the code.
def highlight_keywords(master):
    master.editor.tag_config("test_tag", foreground="#E98400")

    start_index = '1.0'
    while True:
        match_length = IntVar()
        index = master.editor.search(pattern=exact_keyword('for'), exact=True, count=match_length, index=start_index,
                                     regexp=True, forwards=True, stopindex=END)
        print(index, match_length.get())

        if index == '':
            break
        if match_length.get() == 0:
            break

        index_split = str(index).split('.')
        row, column = index_split[0], index_split[1]
        end_index = row + '.' + str(int(column) + match_length.get())
        master.editor.tag_add("test_tag", index, end_index)
        start_index = end_index

    # https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
    master.after(master.ENV_RECOLORING_TIME, lambda: highlight_keywords(master))


#  Asks user for an integer which is the number of times to run script
class AskForNumberOfRunsWindow(object):
    def __init__(self, master):
        self.top_window = Toplevel(master)
        self.message = Label(self.top_window, text="How many times to run the script?")
        self.message.pack()
        self.input_box = Entry(self.top_window)
        self.input_box.pack()
        self.button_box = Button(self.top_window, text='Run code', command=self.cleanup)
        self.button_box.pack()
        self.number_of_executions = 0

    def cleanup(self):
        self.number_of_executions = self.input_box.get()
        self.top_window.destroy()


# =====================================
# The whole GUI as a Class.
# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # Set basic App settings
        self.title('AppCode Student Test Task')
        self.geometry("1200x720")
        self.iconphoto(False, tkinter.PhotoImage(file='kotlin_logo.png'))
        self.resizable(True, True)

        # App env variables
        self.ENV_OPENED_FILE_PATH = ''
        self.ENV_FONT_NAME = "Courier"
        self.ENV_FONT_SIZE = 12
        self.ENV_RECOLORING_TIME = 5000  # time in milliseconds between recoloring
        self.ENV_COLOR = {
            'platinum': '#F7F7F7',
            'dark-grey': '#2B2B2B',
            'grey': '#3C3F41',
            'new-york-pink': '#D16B57'
        }
        self.ENV_TAGS = {

        }

        # Menu bar at the top
        self.menu_bar = Menu(self)

        # Create File button in Menu bar and its options
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', command=lambda: new_file(self))
        self.file_menu.add_command(label='Open', command=lambda: open_file(self))
        self.file_menu.add_command(label='Save', command=lambda: save(self))
        self.file_menu.add_command(label='Save As', command=lambda: save_as(self))
        self.file_menu.add_command(label='Exit', command=exit)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Status bar
        self.status = Label(self, height=1, text="Ready    ", bd=2, relief=FLAT, anchor=E)
        self.status.pack(side=BOTTOM, fill=X)

        # Create run button in Menu bar
        self.run_bar = Menu(self.menu_bar, tearoff=0)
        self.run_bar.add_command(label='Run', command=lambda: Task(self, run, True, ""))
        self.run_bar.add_command(label='Save & Run', command=lambda: save_and_run(self))
        self.run_bar.add_command(label='Run Multiple Times',
                                 command=lambda: TaskToRunSimultaneously(self, run_multiple_times))
        self.run_bar.add_command(label='Save & Run Multiple Times',
                                 command=lambda: save_and_run_multiple_times(self))
        self.menu_bar.add_cascade(label='Run', menu=self.run_bar)

        # Code output pane with vertical scroll bar
        code_output_frame = Frame(self)
        code_output_frame.pack(side=BOTTOM, fill=X)
        self.output_pane_scrollbar = tkinter.Scrollbar(code_output_frame)
        self.code_output = Text(code_output_frame, state=DISABLED, bg=self.ENV_COLOR['dark-grey'],
                                fg=self.ENV_COLOR['platinum'], height=10,
                                font=(self.ENV_FONT_NAME, self.ENV_FONT_SIZE),
                                yscrollcommand=self.output_pane_scrollbar.set)

        self.output_pane_scrollbar.config(command=self.code_output.yview)
        self.output_pane_scrollbar.pack(side=RIGHT, fill=Y)
        self.code_output.pack(side=BOTTOM, fill=X)

        # Editor Pane with vertical scroll bar
        self.editor_pane_scrollbar = tkinter.Scrollbar(self)
        self.editor = Text(bg=self.ENV_COLOR['grey'], fg=self.ENV_COLOR['platinum'],
                           font=("Courier", self.ENV_FONT_SIZE), height=100, width=200,
                           insertbackground='white', undo=True, yscrollcommand=self.editor_pane_scrollbar.set)

        self.editor_pane_scrollbar.config(command=self.editor.yview)
        self.editor_pane_scrollbar.pack(side=RIGHT, fill=Y)
        self.editor.pack(side=TOP, fill=X, expand=True)

        # Make menu bar appear
        self.config(menu=self.menu_bar)

        # Create tags to color some parts of the code or output
        self.code_output.tag_config("error", foreground=self.ENV_COLOR['new-york-pink'])
        self.editor.tag_config("test_tag", foreground="blue")

        highlight_keywords(self)


# main
if __name__ == "__main__":
    App().mainloop()
