import tkinter as tk
from tkinter import scrolledtext
from tkinter import Toplevel, Label


class ChatInterface:
    def __init__(self, send_callback, title="GPT AI"):
        self.send_callback = send_callback
        self.window = tk.Tk()
        self.window.title(title)

        self.setup_window()
        self.display_bot_message("안녕하세요. 무엇을 도와드릴까요?")

    def setup_window(self):
        font = ("맑은 고딕", 10)

        self.conversation = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, bg='#f0f0f0', font=font)
        self.conversation.tag_configure("user", background="#c9daf8")
        self.conversation.tag_configure("assistant", background="#e4e4e4")
        self.conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        input_frame = tk.Frame(self.window)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_entry = tk.Entry(input_frame)
        self.user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.user_entry.bind('<Return>', lambda event: self.on_send())

        send_button = tk.Button(input_frame, text="Send", command=self.on_send)
        send_button.pack(side=tk.RIGHT)

    def display_message(self, message, tag):
        self.conversation.config(state=tk.NORMAL)
        self.conversation.insert(tk.END, message, tag)
        self.conversation.config(state=tk.DISABLED)
        self.conversation.see(tk.END)

    def display_bot_message(self, message):
        self.display_message(f"Bot: {message}\n", "assistant")

    def on_send(self):
        user_input = self.user_entry.get()
        self.user_entry.delete(0, tk.END)
        self.display_message(f"You: {user_input}\n", "user")
        self.send_callback(user_input)

    def show_popup(self, message):
        self.popup = Toplevel(self.window)
        self.popup.title("Message")
        Label(self.popup, text=message).pack(pady=10, padx=10)

    def close_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None

    def run(self):
        self.window.mainloop()

