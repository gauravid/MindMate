# 🧠 MindMate – Mental Wellness Chatbot

MindMate is a Flask-based NLP chatbot that helps users track and understand their emotional well-being through real-time conversation and motivational support.

## 💡 Features

- Emotion detection using HuggingFace's `bert-base-uncased-emotion`
- Personalized motivational quotes via `distilgpt2`
- User-specific emotion history and visual charting (Matplotlib)
- MySQL-based chat and emotion logging
- Responsive, modern UI built with HTML/CSS/JS

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/mindmate.git
cd mindmate
pip install -r requirements.txt
