# 🧠 MindMate - Student Mental Wellness Chatbot

MindMate is an NLP-powered chatbot designed to support students' mental health by providing emotionally intelligent responses, affirmations, and helpful tips based on detected emotions.

## 🌟 Features

- 💬 Emotion-aware chatbot using a Hugging Face transformer model
- ⏰ Time-based greeting system (morning/afternoon/evening)
- 🌈 Responsive and soothing frontend UI with cheerful avatar
- 📘 Non-repetitive affirmations and emotion-specific tips
- 🗃️ MySQL database integration for chat history logging
- 📞 Built-in helpline support panel with verified mental health contacts

## 🛠️ Tools & Technologies Used

- Python, Flask
- Hugging Face Transformers (BERT-based emotion model)
- HTML, CSS, JavaScript
- MySQL, mysql-connector-python

## 🧑‍💻 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/mindmate.git
   cd mindmate
   ```

2. **Install dependencies**
   ```bash
   pip install flask transformers mysql-connector-python
   ```

3. **Setup MySQL Database**
   - Start your MySQL server and run the contents of `schema.sql` file in your MySQL client.
   - Make sure your DB credentials in `app.py` match your system.

4. **Run the App**
   ```bash
   python app.py
   ```

5. **Access it in browser**
   ```
   http://localhost:5000/
   ```

## 🗃️ Database Tables

- `users`: For optional multi-user support
- `messages`: Logs each message with emotion tags
- `emotions`: Optional emotion descriptions
- `chat_history`: Logs basic chat exchanges

## 🤝 Contributing

Pull requests and suggestions are welcome!

## 📄 License

This project is for academic and demonstration purposes.
