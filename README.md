## 🗝️🔗 How to Generate Your Own Google Gemini API Key via Google AI Studio

1. 🌐 Go to [Google AI Studio](https://aistudio.google.com/).
2. 👤 Sign in with your Google account.
3. 🏷️ Click on "Get API Key" or navigate to the API section.
4. ⚙️ Follow the prompts to enable the Gemini API and create a new API key.
5. 📋 Copy your API key.
6. 💾 In this project, open `bot.py`, and replace the value of `self.api_key` with your own API key.
7. 🚀 Save the file and relaunch your chatbot for secure, personalized access.

> 🔒 **Keep your API key secret.** Never share it publicly or commit it to public repositories.


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
