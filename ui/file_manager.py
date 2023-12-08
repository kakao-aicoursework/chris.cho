import tkinter.filedialog as filedialog

def open_file_dialog():
    return filedialog.askopenfilename()

def save_file_dialog():
    return filedialog.asksaveasfilename()