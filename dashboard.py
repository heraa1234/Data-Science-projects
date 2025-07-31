import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set file path
file_path = "output_chat_analysis.csv"

if not os.path.exists(file_path):
    print(f"❌ File '{file_path}' not found.")
    exit()

# Load data
df = pd.read_csv(file_path)

# Rename columns to match expected names
df.rename(columns={
    "Timestamp": "timestamp",
    "Emotion": "emotion",
    "Sentiment Score": "sentiment",
    "Travel Intent": "mentions_travel"
}, inplace=True)

# Convert timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', dayfirst=True)

# Convert travel intent to boolean
df['mentions_travel'] = df['mentions_travel'].apply(lambda x: x.strip().lower() == "travel")

# Create date column
df['date'] = df['timestamp'].dt.date

# Create output folder if not exists
os.makedirs("visualizations", exist_ok=True)

# Sentiment distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["sentiment"], bins=10, kde=True, color="skyblue")
plt.title("Sentiment Score Distribution")
plt.xlabel("Sentiment Score")
plt.tight_layout()
plt.savefig("visualizations/sentiment_distribution.png")
plt.close()

# Emotion distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="emotion", palette="magma")
plt.title("Emotion Distribution")
plt.xlabel("Emotion")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("visualizations/emotion_distribution.png")
plt.close()

# Travel mentions over time
travel_df = df[df["mentions_travel"] == True]

if not travel_df.empty:
    travel_count = travel_df.groupby("date").size()
    plt.figure(figsize=(10, 5))
    travel_count.plot(kind="bar", color="teal")
    plt.title("Mentions of Travel Over Time")
    plt.xlabel("Date")
    plt.ylabel("Mentions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visualizations/travel_mentions_over_time.png")
    plt.close()
else:
    print("⚠️ No travel mentions found for visualization.")

print("✅ Visualizations saved to 'visualizations/' folder.")
