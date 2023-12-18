import sys
import tkinter as tk
from tkinter import scrolledtext
import subprocess

# macOS 다크 모드 활성화 여부를 확인하는 함수
def is_dark_mode():
    try:
        # macOS의 다크 모드 설정 값을 읽어 옵니다.
        mode = subprocess.check_output('defaults read -g AppleInterfaceStyle', shell=True)
        return mode.strip().decode() == 'Dark'
    except subprocess.CalledProcessError:
        # 명령어 실행에 실패하면 다크 모드가 아닌 것으로 간주
        return False

# 다크 모드와 라이트 모드에 따른 색상 설정
def get_mode_colors():
    if is_dark_mode():
        # 다크 모드용 색상
        return {
            "bg": "#1e1e1e",
            "user": "#3c5c8d",
            "assistant": "#2c2c2c",
        }
    else:
        # 라이트 모드용 색상
        return {
            "bg": "#f0f0f0",
            "user": "#c9daf8",
            "assistant": "#e4e4e4",
        }
class ChatInterface:
    def __init__(self, send_callback, title="GPT AI"):
        self.send_callback = send_callback
        self.window = tk.Tk()
        self.window.title(title)

        self.setup_window()
        self.display_bot_message("[조건우] 안녕하세요. 챗봇 서비스를 시작합니다. 궁금하신 내용을 물어보세요?")

    def setup_window(self):
        colors = get_mode_colors()
        font = ("맑은 고딕", 16)
        self.conversation = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, bg=colors['bg'], font=font)
        self.conversation.tag_configure("user", background=colors['user'])
        self.conversation.tag_configure("assistant", background=colors['assistant'])
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

    def display_bot_message(self, message, bot_name='AI Bot'):
        self.display_message(f"{bot_name}: {message}\n", "assistant")

    def on_send(self):
        user_input = self.user_entry.get()
        self.user_entry.delete(0, tk.END)
        self.display_message(f"You: {user_input}\n", "user")
        self.send_callback(user_input)

    def show_loading_popup(self):
        self.popup = self._show_popup_message(self.window, "처리중...")
        pass
    def close_loading_popup(self):
        self.popup.destroy()
        pass

    def _show_popup_message(self, window, message):
        popup = tk.Toplevel(window)
        popup.title("")

        # 팝업 창의 내용
        label = tk.Label(popup, text=message, font=("맑은 고딕", 12))
        label.pack(expand=True, fill=tk.BOTH)

        # 팝업 창의 크기 조절하기
        window.update_idletasks()
        popup_width = label.winfo_reqwidth() + 20
        popup_height = label.winfo_reqheight() + 20
        popup.geometry(f"{popup_width}x{popup_height}")

        # 팝업 창의 중앙에 위치하기
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f"+{popup_x}+{popup_y}")

        popup.transient(window)
        popup.attributes('-topmost', True)

        popup.update()
        return popup

    def run(self):
        self.window.mainloop()