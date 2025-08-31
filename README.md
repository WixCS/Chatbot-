
# 🤖 Gemini Chatbot

A modern, smooth, and user-friendly AI chatbot built with Python, Tkinter, and Google Gemini API. The interface mimics popular chat tools, providing concise, point-wise, and visually appealing responses.

## ✨ Features
- 🖥️ Clean, modern GUI with custom fonts and colors
- 💬 Streams AI responses word by word for realism
- 📋 Point-wise, concise answers (100 words by default, with "Show More" for longer replies)
- 🔒 No API key prompt (API key is hardcoded for demo purposes)
- 🧑‍💻 Clear separation of user and bot messages
- ⚡ Error handling and smooth user experience

## 🚀 Setup

1. 📥 **Clone or download this repository.**
2. 🐍 **Create a Python virtual environment (optional but recommended):**
   ```powershell
   python -m venv iitp_env
   .\iitp_env\Scripts\activate
   ```
3. 📦 **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. ▶️ **Run the chatbot:**
   ```powershell
   python bot.py
   ```

## 📝 Requirements
- Python 3.8+
- 🌐 Internet connection (for Google Gemini API)

## 🎨 Customization
- ✏️ To use your own Google Gemini API key, replace the value of `self.api_key` in `bot.py`.
- 🎨 You can further style the UI by editing the color and font variables in `bot.py`.

## 📄 License
This project is for educational/demo purposes. Replace the API key with your own for production use.
