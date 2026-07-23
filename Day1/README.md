# Gemini CLI Chatbot

A simple, interactive command-line interface (CLI) chatbot built with Python and Google's Gemini API (`gemini-1.5-flash`).

---

## Features

* **Terminal Chat Interface:** Simple loop allowing for a continuous conversation.
* **Gemini Integration:** Powered by the `gemini-1.5-flash` model.
* **Error Handling:** Gracefully handles missing API keys and runtime exceptions.

---

## Prerequisites

* **Python 3.8+**
* **Google Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/))

---

## Installation & Setup

1. **Clone or download this repository** to your local machine (ideally inside your project folder with a virtual environment active):

   ```bash
   git clone <repository-url>

2. **Install the required package:***

    ```bash
    pip install google-generativeai


3. Set your API Key environment variable:
macOS / Linux:

    ```bash
    export GEMINI_API_KEY="your_actual_api_key_here"
Windows (Command Prompt):

    ```bash
    set GEMINI_API_KEY=your_actual_api_key_here

---

## How to Run
- Execute the main script from your terminal:

    ```bash
    python geminiAPIcode.py

Type your message and press Enter to chat.
Type quit or exit to end the session.

Write this in mardown formt as well with all the syntax