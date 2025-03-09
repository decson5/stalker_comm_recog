# Import libraries for Telegram bot, data processing, and modeling
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from telegram.ext import Application, CommandHandler

# Telegram bot token and chat ID
TOKEN = "Token_here"
CHAT_ID = None # Place your Chat_Id here

# Load and train the model once at startup
df = pd.read_csv("stalker_reviews.csv")  # Use new balanced dataset
X = df["Text"]
y = df["Label"]

# Print class distribution to check balance
print(f"Total reviews: {len(df)}")
print(f"Positive reviews: {sum(y == 'positive')}")
print(f"Negative reviews: {sum(y == 'negative')}")

# Convert text data into numerical features using Tfidf with bigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_vector = vectorizer.fit_transform(X)

# Initialize and train the SVM model
model = LinearSVC()
scores = cross_val_score(model, X_vector, y, cv=5)
print(f"Average accuracy from cross-validation: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})")
model.fit(X_vector, y)

# Handler for /start command
async def start(update, context):
    await update.message.reply_text("Hello! I'm a bot that classifies S.T.A.L.K.E.R. 2 reviews. Use /classify <text> to check a review!")

# Handler for /classify command
async def classify_text(update, context):
    text = update.message.text.replace("/classify ", "")
    if text == "/classify":
        await update.message.reply_text("Please provide a review after /classify, e.g., '/classify This game is awesome!'")
        return
    
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    await update.message.reply_text(f"This is a {prediction} review!")

# Main function to set up and run the bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("classify", classify_text))
    
    print("Bot is running! Send /start or /classify to use it.")
    app.run_polling()

if __name__ == "__main__":
    main()