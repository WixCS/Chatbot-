
import tkinter as tk
from tkinter import scrolledtext, messagebox
from google import genai
from google.genai import types


class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Chatbot")
        self.root.configure(bg="#222831")

        # Theme & style
        self.font_family = "Segoe UI"
        self.user_color = "#00adb5"
        self.bot_color = "#eeeeee"
        self.bg_color = "#222831"
        self.entry_bg = "#393e46"
        self.button_bg = "#00adb5"
        self.button_fg = "#222831"

        # API setup
        self.api_key = "YOUR_API"
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize client: {e}")
            root.destroy()
            return

        self.model = "gemini-2.5-flash-lite"
        self.create_widgets()

    def create_widgets(self):
        # Chat area
        chat_frame = tk.Frame(self.root, bg=self.bg_color)
        chat_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            state='disabled',
            width=60,
            height=20,
            font=(self.font_family, 12),
            bg=self.bg_color,
            fg=self.bot_color,
            insertbackground=self.bot_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        # Entry & button
        entry_frame = tk.Frame(self.root, bg=self.bg_color)
        entry_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.entry = tk.Entry(
            entry_frame,
            font=(self.font_family, 12),
            bg=self.entry_bg,
            fg=self.bot_color,
            insertbackground=self.bot_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        self.entry.bind('<Return>', lambda event: self.send_message())

        send_button = tk.Button(
            entry_frame,
            text="Send",
            command=self.send_message,
            font=(self.font_family, 12, "bold"),
            bg=self.button_bg,
            fg=self.button_fg,
            borderwidth=0,
            padx=20,
            pady=6,
            cursor="hand2"
        )
        send_button.pack(side=tk.LEFT)

    def display_message(self, message, sender="bot"):
        self.chat_area.config(state='normal')
        tag = 'user' if sender == "user" else 'bot'
        self.chat_area.insert(tk.END, message + "\n", tag)
        self.chat_area.tag_config('user', foreground=self.user_color, font=(self.font_family, 12, "bold"))
        self.chat_area.tag_config('bot', foreground=self.bot_color, font=(self.font_family, 12))
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.display_message("You: " + user_input, sender="user")
        self.entry.delete(0, tk.END)
        self.root.after(100, lambda: self.get_bot_response(user_input))

    def get_bot_response(self, user_input):
        try:
            contents = [
                types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
            ]
            response_text = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents
            ):
                if hasattr(chunk, 'text'):
                    response_text += chunk.text
            self.display_message("Bot: " + response_text.strip(), sender="bot")
        except Exception as e:
            self.display_message(f"Bot: [Error: {e}]", sender="bot")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()


