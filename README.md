# stalker_comm_recog
# S.T.A.L.K.E.R. 2 Review Classifier
A Telegram bot that classifies Steam reviews for S.T.A.L.K.E.R. 2 as positive or negative using machine learning.

## Features
- Scrapes 2000 reviews from Steam API.
- Uses SVM with TF-IDF (bigrams) for classification.
- Accuracy: 84% (±3%) via 5-fold cross-validation.
- Telegram bot with /classify command.

## How to Run
1. Install: `pip install pandas scikit-learn python-telegram-bot requests`.
2. Run `scrape_stalker.py` to fetch reviews.
3. Update `TOKEN` and `CHAT_ID` in `stalker_bot.py`.
4. Run `stalker_bot.py` to start the bot.

## Example
- `/classify The game is trash!` → "This is a negative review!"
- `/classify The game is so good!` → "This is a positive review!"

## Why It's Cool for S.T.A.L.K.E.R. 2
This bot acts like a trusty companion exploring the Zone of reviews for S.T.A.L.K.E.R. 2. It knows where players uncover "artifacts" of praise—like the gripping atmosphere—and where they stumble into "anomalies" of frustration, such as bugs or lag. All this insight comes from analyzing 2000 real Steam reviews, making it a handy tool for understanding what the community thinks about the game!
