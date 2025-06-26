from flask import Flask, render_template, request, jsonify
import mysql.connector
import random
from transformers import pipeline
from datetime import datetime

app = Flask(__name__)

# Load HuggingFace emotion model
emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")

# DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gauru@9422",
    database="mindmate",
)
cursor = conn.cursor()

# Emotion Mapping
emotion_mapping = {
    "joy": "happy", "sadness": "sad", "anger": "angry", "fear": "anxious",
    "love": "tips", "surprise": "more", "disgust": "overwhelmed", "neutral": "neutral",
    "confused": "confused", "bored": "bored", "guilt": "guilt", "shame": "shame",
    "excitement": "excited", "burnout": "burnout", "insecure": "insecure", "disappointment": "disappointed"
}

# Manual emotion keywords for override
manual_emotion_keywords = {
    "burnout": "burnout", "exhausted": "burnout", "tired": "burnout",
    "shame": "shame", "ashamed": "shame",
    "guilt": "guilt", "guilty": "guilt",
    "insecure": "insecure", "disappointed": "disappointed",
    "confused": "confused", "bored": "bored"
}

# Affirmations
emotional_responses = {
    "happy": ["That's great to hear! Keep nurturing that positive energy."],
    "sad": ["It’s okay to feel sad. I’m here with you.", "Let those emotions flow. You're safe here."],
    "anxious": ["That sounds tough. You’re not alone.", "Breathe, you're doing better than you think."],
    "angry": ["Your emotions are valid. This is a safe space.", "Let it out—I'm here for you."],
    "lonely": ["You’re not alone in this. Let’s talk."],
    "not well": ["I'm here for you. Let's take it one step at a time."],
    "stressed": ["That’s a lot to carry. I’m here with you."],
    "overwhelmed": ["Take a breath. You’re doing your best.", "You don’t have to do it all at once."],
    "confused": ["It's okay to forget sometimes. Let’s figure it out together.", "We’ll make sense of it together."],
    "bored": ["Maybe we can explore something new."],
    "neutral": ["Whenever you're ready to talk, I’m here."],
    "guilt": ["It’s okay to feel guilt — you're human.", "Let's learn and grow through it."],
    "shame": ["You’re still worthy no matter how you feel."],
    "excited": ["That’s amazing! Let’s celebrate this moment!"],
    "burnout": ["You've been pushing hard. Let’s pause and recharge."],
    "insecure": ["Everyone has doubts — you're not alone.", "You're stronger than you think."],
    "disappointed": ["It's okay to feel let down. Let’s talk about it."],
    "tips": [], "more": []
}

# Tips
emotion_tips = {
    "sad": ["Write your feelings down.", "Connect with a friend.", "Watch something comforting."],
    "anxious": ["Inhale for 4, hold for 4, exhale for 4.", "Try grounding: 5-4-3-2-1 technique."],
    "angry": ["Take deep breaths.", "Try journaling or walking."],
    "confused": ["Break it into small pieces.", "Speak out loud to clarify thoughts."],
    "bored": ["Change your environment.", "Try a 10-min hobby."],
    "overwhelmed": ["List 3 top tasks only.", "Take a proper break."],
    "stressed": ["Use Pomodoro method.", "Stretch between tasks."],
    "lonely": ["Reach out to someone.", "Try group activities online."],
    "neutral": ["Journal how you feel.", "Reflect on your week."],
    "happy": ["Start a gratitude list.", "Share your joy!"],
    "guilt": ["Write about what happened.", "Practice self-forgiveness."],
    "shame": ["Talk to someone kind.", "You are not your mistakes."],
    "excited": ["Channel it into something creative.", "Use that momentum!"],
    "burnout": ["Unplug and rest.", "Say no to extra tasks."],
    "insecure": ["List your strengths.", "Stop comparing yourself."],
    "disappointed": ["Acknowledge your feelings.", "Make a fresh small goal."],
    "tips": ["Eat well, rest, hydrate.", "Avoid too much screen time."],
    "more": ["Try meditation apps.", "Speak with a counselor if needed."]
}

user_state = {"stage": "init", "emotion": None, "last_affirms": []}

def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning! 🌞"
    elif 12 <= hour < 17:
        return "Good afternoon! ☀️"
    elif 17 <= hour < 21:
        return "Good evening! 🌇"
    else:
        return "Hope you're doing okay this late. 🌙"

def get_response(user_message):
    user_message = user_message.lower().strip()

    if "bye" in user_message:
        user_state["stage"] = "init"
        user_state["last_affirms"] = []
        return "Goodbye! 😊 Take care and remember, you're doing your best. I'm always here if you need to talk again."

    greetings = ["hi", "hello", "hey", "hlo", "good morning", "good evening"]
    if user_message in greetings:
        user_state["stage"] = "emotion_check"
        user_state["emotion"] = None
        user_state["last_affirms"] = []
        greeting = get_time_based_greeting()
        return (
            f"{greeting} I'm MindMate. 😊\n"
            "How are you feeling today? You can type how you feel or choose from:\n"
            "- Joy\n- Sad\n- Angry\n- Anxious\n- Lonely\n- Stressed\n- Overwhelmed\n- Bored\n- Confused\n- Guilt\n- Shame\n- Excited\n- Burnout\n- Insecure\n- Disappointed"
        )

    if user_state["stage"] == "emotion_check":
        for keyword, manual_emotion in manual_emotion_keywords.items():
            if keyword in user_message:
                user_state["emotion"] = manual_emotion
                user_state["stage"] = "response_options"
                affirm = random.choice(emotional_responses.get(manual_emotion, ["I'm here with you."]))
                save_message(user_message, affirm)
                return f"{affirm}\nWould you like to *share* or get some *tips*?"
        try:
            prediction = emotion_classifier(user_message)
            emotion_label = prediction[0]["label"]
            mapped_emotion = emotion_mapping.get(emotion_label, "neutral")
            user_state["emotion"] = mapped_emotion
            user_state["stage"] = "response_options"
            affirm = random.choice(emotional_responses.get(mapped_emotion, ["I'm here with you."]))
            save_message(user_message, affirm)
            return f"{affirm}\nWould you like to *share* or get some *tips*?"
        except:
            return "Oops! I had trouble understanding that. Could you say it differently?"

    if user_state["stage"] == "response_options":
        if "share" in user_message:
            user_state["stage"] = "listening"
            return "I'm listening. When you're done, just say *done*."
        elif "tip" in user_message:
            tips_list = emotion_tips.get(user_state["emotion"], emotion_tips["tips"])
            user_state["stage"] = "after_tips"
            return f"Here are some tips:\n- " + "\n- ".join(tips_list) + "\nWould you like to *share* something, *talk more*, or say *bye*?"

    if user_state["stage"] == "listening":
        if "done" in user_message:
            tips_list = emotion_tips.get(user_state["emotion"], emotion_tips["tips"])
            user_state["stage"] = "after_tips"
            return f"Thanks for sharing. 💬\nHere are some tips for you:\n- " + "\n- ".join(tips_list) + "\nWould you like to *continue* sharing or say *bye*?"
        else:
            # Non-repeating affirmations
            emotion = user_state["emotion"]
            all_affirms = emotional_responses.get(emotion, ["I'm here for you."])
            used_affirms = user_state.get("last_affirms", [])
            remaining_affirms = [a for a in all_affirms if a not in used_affirms]
            if not remaining_affirms:
                user_state["last_affirms"] = []
                remaining_affirms = all_affirms
            affirm = random.choice(remaining_affirms)
            user_state["last_affirms"].append(affirm)
            return f"{affirm}\n(When you're done, just type *done*)"

    if user_state["stage"] == "after_tips":
        if any(word in user_message for word in ["share", "talk", "continue"]):
            user_state["stage"] = "listening"
            return "Sure, I’m still listening. Please continue. 💬"
        elif "no" in user_message or "nothing" in user_message:
            user_state["stage"] = "init"
            user_state["last_affirms"] = []
            return "No worries. I'm here if you ever want to talk again. Take care! 😊"
        else:
            return "Would you like to *share* more or say *bye*?"

    return "I'm here to support you. You can type *share*, *tips*, *continue*, or say *bye* anytime."

def save_message(user_msg, bot_response):
    cursor.execute("INSERT INTO chat_history (user_message, bot_response) VALUES (%s, %s)", (user_msg, bot_response))
    conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "").strip()
    if not user_message:
        return jsonify(response="Please enter a message.")
    response = get_response(user_message)
    return jsonify(response=response)

if __name__ == "__main__":
    app.run(debug=True)
