# To run this code you need to install the following dependencies:
# pip install google-genai


# --- GUI Chatbot using Tkinter ---
import os
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
from google import genai
from google.genai import types


class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Chatbot")
        self.root.configure(bg="#222831")
        self.font_family = "Segoe UI"
        self.user_color = "#00adb5"
        self.bot_color = "#eeeeee"
        self.bg_color = "#222831"
        self.entry_bg = "#393e46"
        self.button_bg = "#00adb5"
        self.button_fg = "#222831"
        # Use hardcoded API key, do not prompt user
        self.api_key = "Enter the API here"
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize client: {e}")
            root.destroy()
            return
        self.model = "gemini-2.5-flash-lite"
        self.create_widgets()

    def create_widgets(self):
        # Chat area frame
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
        self.chat_area.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

        # Entry and send button frame
        entry_frame = tk.Frame(self.root, bg=self.bg_color)
        entry_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.entry = tk.Entry(
            entry_frame,
            width=50,
            font=(self.font_family, 12),
            bg=self.entry_bg,
            fg=self.bot_color,
            insertbackground=self.bot_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 10), pady=0, expand=True, fill=tk.X)
        self.entry.bind('<Return>', lambda event: self.send_message())

        self.send_button = tk.Button(
            entry_frame,
            text="Send",
            command=self.send_message,
            font=(self.font_family, 12, "bold"),
            bg=self.button_bg,
            fg=self.button_fg,
            activebackground=self.user_color,
            activeforeground=self.bg_color,
            borderwidth=0,
            highlightthickness=0,
            padx=20,
            pady=6,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 0), pady=0)

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.display_message("You: " + user_input, sender="user")
        self.entry.delete(0, tk.END)
        self.root.after(100, lambda: self.get_bot_response(user_input))

    def show_full_response(self, full_response):
        self.display_message("Bot: " + full_response.strip(), sender="bot", bold=True, newlines=True)
        if hasattr(self, 'show_more_button'):
            self.show_more_button.destroy()

    def display_message(self, message, sender="bot", bold=False, newlines=False):
        self.chat_area.config(state='normal')
        tag = 'user' if sender == "user" else 'bot_bold' if bold else 'bot'
        # Always add a blank line before user and bot messages for separation, except for the very first message
        if float(self.chat_area.index('end-1c')) > 1.0:
            self.chat_area.insert(tk.END, '\n')
        if newlines and sender == "bot":
            # Split by points for bot answers, remove asterisks and bullets, use new lines
            points = [pt.strip().lstrip('*•-0123456789. ') for pt in message.split("\n") if pt.strip()]
            for pt in points:
                self.chat_area.insert(tk.END, pt + '\n', tag)
        else:
            self.chat_area.insert(tk.END, message + '\n', tag)
        self.chat_area.tag_config('user', foreground=self.user_color, font=(self.font_family, 12, "bold"))
        self.chat_area.tag_config('bot', foreground=self.bot_color, font=(self.font_family, 12))
        self.chat_area.tag_config('bot_bold', foreground=self.bot_color, font=(self.font_family, 12, "bold"))
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def get_bot_response(self, user_input):
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_input)],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            )
            response = ""
            # Stream and display word by word for smoothness
            def stream_words(text):
                words = text.split()
                for i, word in enumerate(words):
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, (word + ' '), 'bot_bold')
                    self.chat_area.config(state='disabled')
                    self.chat_area.see(tk.END)
                    self.root.update()
                    if i % 5 == 0:
                        self.root.after(10)

            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if hasattr(chunk, 'text'):
                    response += chunk.text
                elif hasattr(chunk, 'candidates') and chunk.candidates:
                    response += chunk.candidates[0].text

            words = response.strip().split()
            if len(words) > 100 and not ("more" in user_input.lower() or "continue" in user_input.lower()):
                short_response = ' '.join(words[:100]) + '...'
                # Try to format as points if possible
                if '\n' in short_response or any(bullet in short_response for bullet in ['1.', '2.', '•', '-']):
                    self.display_message("Bot: " + short_response, sender="bot", bold=True, newlines=True)
                else:
                    stream_words(short_response)
                # Add a Show More button
                if hasattr(self, 'show_more_button'):
                    self.show_more_button.destroy()
                self.show_more_button = tk.Button(
                    self.root,
                    text="Show More",
                    command=lambda: self.show_full_response(response.strip()),
                    font=(self.font_family, 10, "bold"),
                    bg=self.button_bg,
                    fg=self.button_fg,
                    activebackground=self.user_color,
                    activeforeground=self.bg_color,
                    borderwidth=0,
                    highlightthickness=0,
                    padx=10,
                    pady=3,
                    cursor="hand2"
                )
                self.show_more_button.pack(pady=(0, 10))
            else:
                # Try to format as points if possible
                if '\n' in response or any(bullet in response for bullet in ['1.', '2.', '•', '-']):
                    self.display_message("Bot: " + response.strip(), sender="bot", bold=True, newlines=True)
                else:
                    stream_words(response.strip())
                if hasattr(self, 'show_more_button'):
                    self.show_more_button.destroy()
        except Exception as e:
            self.display_message(f"Bot: [Error: {e}]", sender="bot", bold=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()

