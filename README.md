# 🧠 MindMate — Mental Wellness Chatbot

**MindMate** is a web-based mental wellness chatbot that uses Natural Language Processing (NLP) to detect users' emotions from their messages and respond supportively. It also visualizes emotional trends over time to help users better understand their mental state.

---

## 💡 Features

- 🗣️ Chatbot with HuggingFace emotion detection (`bert-base-uncased-emotion`)
- 💬 Stores user conversations and emotion labels in MySQL
- 📊 Emotion statistics and personalized emotion history with visual charts
- 🧠 Emotion-based motivational tips and responses
- 🧾 Session-based tracking without login (auto-generated user ID)
- 🛠️ Admin dashboard for emotion trends across all users

---

## 🛠️ Tech Stack

| Layer        | Tech                       |
|-------------|----------------------------|
| Frontend    | HTML, CSS, JavaScript (Jinja templates) |
| Backend     | Python, Flask              |
| Database    | MySQL                      |
| ML/NLP      | HuggingFace Transformers   |
| Visualization | Matplotlib               |

---


