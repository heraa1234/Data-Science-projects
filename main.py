import re
import pandas as pd
from textblob import TextBlob
import os
import emoji

# === CONFIG ===
file_path = r"C:\bonviaj\Whatsapp_analyzer\whatsapp_chat.txt"  # Change this if needed
output_csv = "output_chat_analysis.csv"

# === EMOTION DETECTION ===
def detect_emotion(message):
    message_lower = message.lower()
    if any(word in message_lower for word in ["happy", "great", "awesome", "fun", "joy", "😊", "😁", "😃"]):
        return "Positive"
    elif any(word in message_lower for word in ["sad", "cry", "depressed", "unhappy", "😢", "😭"]):
        return "Negative"
    elif any(word in message_lower for word in ["angry", "mad", "annoyed", "😠", "😡"]):
        return "Angry"
    elif any(word in message_lower for word in ["bored", "meh", "😐"]):
        return "Neutral"
    else:
        return "Unknown"

# === TRAVEL DETECTION ===
def detect_travel_intent(message):
    keywords = ["trip", "travel", "journey", "vacation", "holiday", "going to", "visit", "flight", "book tickets", "goa", "manali"]
    if any(word in message.lower() for word in keywords):
        if "friends" in message.lower() or "group" in message.lower():
            return "Friends Trip"
        return "Travel Mentioned"
    return "No Travel"

# === WHATSAPP CHAT PARSER ===
def parse_whatsapp_chat(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()

    messages = []
    date_pattern = r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?: [APMapm]{2})? - '

    for line in lines:
        if re.match(date_pattern, line):
            parts = line.split(" - ", 1)
            if len(parts) == 2:
                timestamp = parts[0]
                content = parts[1]
                if ": " in content:
                    sender, message = content.split(": ", 1)
                    messages.append((timestamp, sender, message.strip()))
    return messages

# === MAIN ANALYSIS FUNCTION ===
def analyze_chat(messages):
    records = []

    for ts, sender, msg in messages:
        sentiment = TextBlob(msg).sentiment.polarity
        emotion = detect_emotion(msg)
        travel = detect_travel_intent(msg)
        topic = "Travel" if travel != "No Travel" else "General"
        records.append({
            "Timestamp": ts,
            "Sender": sender,
            "Message": msg,
            "Emotion": emotion,
            "Sentiment Score": sentiment,
            "Travel Intent": travel,
            "Topic": topic
        })

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    return df

# === RUN ===
if __name__ == "__main__":
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
    else:
        messages = parse_whatsapp_chat(file_path)
        if not messages:
            print("No messages extracted. Make sure it's a valid WhatsApp export.")
        else:
            df = analyze_chat(messages)
            print(f"✅ Analysis complete. {len(df)} messages saved to {output_csv}.")

            # Summary stats
            print("\n📊 Summary:")
            print(df["Emotion"].value_counts())
            print("\nTravel Mentions:")
            print(df["Travel Intent"].value_counts())
