import random
import openai
from datetime import datetime
from flask import session
from transformers import pipeline

from config import emotion_mapping, manual_emotion_keywords, emotional_responses, emotion_tips

emotion_classifier = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")
generator = pipeline("text-generation", model="distilgpt2")
user_state = {"stage": "init", "emotion": None, "last_affirms": []}

def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning! 🌞"
    elif 12 <= hour < 17:
        return "Good afternoon! ☀️"
    elif 17 <= hour < 21:
        return "Good evening! 🌇"
    return "Hope you're doing okay this late. 🌙"

def generate_quote(emotion):
    prompt = f"A short motivational quote for someone feeling {emotion}:"
    output = generator(
    prompt,
    max_length=40,
    num_return_sequences=1,
    do_sample=True,
    temperature=1.1,
    top_k=50,
    top_p=0.95
    )
    return output[0]['generated_text'].replace(prompt, '').strip()

def get_response(user_message, user_id, save_message, update_emotion_count, emotion_classifier):
    global user_state
    msg = user_message.lower().strip()

    if "bye" in msg:
        user_state.update({"stage": "init", "last_affirms": []})
        return "Goodbye! 😊 Take care and remember, you're doing your best. I'm always here if you need to talk again."

    greetings = ["hi", "hello", "hey", "hlo", "good morning", "good evening"]

    if user_state["stage"] == "init":
        user_state.update({"stage": "emotion_check", "emotion": None, "last_affirms": []})
        greeting = get_time_based_greeting()
        return f"{greeting} I'm MindMate. 😊\nHow are you feeling today? You can type how you feel or choose from:\n- " + "\n- ".join(emotion_mapping.values())

    if msg in greetings:
        user_state.update({"stage": "emotion_check", "emotion": None, "last_affirms": []})
        return get_time_based_greeting() + " I'm MindMate. 😊\nHow are you feeling today?"

    if user_state["stage"] == "emotion_check":
        for k, emo in manual_emotion_keywords.items():
            if k in msg:
                user_state.update({"emotion": emo, "stage": "response_options"})
                affirm = random.choice(emotional_responses.get(emo, ["I'm here with you."]))
                save_message(msg, affirm, emo)
                update_emotion_count(emo)
                return f"{affirm}\nWould you like to *share* or get some *tips*?"

        try:
            pred = emotion_classifier(msg)
            label = pred[0]["label"]
            score = pred[0]["score"]
            # Treat low-confidence predictions as neutral
            if score < 0.6:
                mapped = "neutral"
            else:
                mapped = emotion_mapping[label] if label in emotion_mapping else "neutral"

            user_state.update({"emotion": mapped, "stage": "response_options"})
            affirm = random.choice(emotional_responses.get(mapped, ["I'm here with you."]))
            save_message(msg, affirm, mapped)
            update_emotion_count(mapped)
            return f"{affirm}\nWould you like to *share* or get some *tips*?"
        except:
            return "Could you rephrase that?"

    if user_state["stage"] == "response_options":
        if "share" in msg:
            user_state["stage"] = "listening"
            return "I'm listening. When you're done, just say *done*."
        if "tip" in msg:
            tips = emotion_tips.get(user_state["emotion"], emotion_tips["tips"])
            user_state["stage"] = "after_tips"
            return f"Here are some tips:\n- " + "\n- ".join(tips) + "\nWould you like to *share* something or say *bye*?"

    if user_state["stage"] == "listening":
        if "done" in msg:
            tips = emotion_tips.get(user_state["emotion"], emotion_tips["tips"])
            quote = generate_quote(user_state["emotion"])
            user_state["stage"] = "after_tips"
            return f"Thanks for sharing. 💬\nHere are some tips:\n- " + "\n- ".join(tips) + f"\n\n🌟 *Quote:* \"{quote}\"\nWould you like to *continue* or say *bye*?"
        affirms = emotional_responses.get(user_state["emotion"], ["I'm here for you."])
        unused = list(set(affirms) - set(user_state["last_affirms"]))
        if not unused:
            user_state["last_affirms"] = []
            unused = affirms
        affirm = random.choice(unused)
        user_state["last_affirms"].append(affirm)
        return f"{affirm}\n(When you're done, type *done*)"

    if user_state["stage"] == "after_tips":
        if any(x in msg for x in ["share", "talk", "continue"]):
            user_state["stage"] = "listening"
            return "Sure, I’m still listening. Please continue. 💬"
        if "no" in msg or "nothing" in msg:
            user_state.update({"stage": "init", "last_affirms": []})
            return "No worries. I'm here if you ever want to talk again. 😊"
        return "Would you like to *share* more or say *bye*?"

    return "I'm here to support you. You can type *share*, *tips*, *continue*, or *bye* anytime."
