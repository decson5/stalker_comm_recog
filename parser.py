# Import libraries for HTTP requests and data handling
import requests
import pandas as pd
import time

# Steam Reviews API endpoint for S.T.A.L.K.E.R. 2 (appid = 1643320)
BASE_URL = "https://store.steampowered.com/appreviews/1643320?json=1"

# Parameters for the API request
params = {
    "filter": "recent",        # Get recent reviews
    "language": "english",     # English reviews only
    "review_type": "all",      # Both positive and negative
    "purchase_type": "all",    # Steam and non-Steam purchases
    "num_per_page": 100,       # Max 100 reviews per request
    "cursor": "*"              # Start from the first page
}

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36"
}

# Function to fetch reviews
def fetch_reviews():
    reviews = []
    explored_cursors = set()
    max_reviews = 2000  # Limit to 2000 reviews for now

    while len(reviews) < max_reviews:
        response = requests.get(BASE_URL, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch reviews. Status code: {response.status_code}")
            break
        
        data = response.json()
        if data["success"] != 1 or not data.get("reviews"):
            print("No more reviews to fetch.")
            break
        
        # Add reviews to the list, handle missing or invalid text
        for review in data["reviews"]:
            text = review.get("review", "No text provided")  # Default if no text
            if not isinstance(text, str) or text.strip() == "":  # Check if text is not a string or empty
                text = "No text provided"
            label = "positive" if review["voted_up"] else "negative"
            reviews.append({"Text": text, "Label": label})
        
        # Update cursor for the next page
        new_cursor = data["cursor"]
        if new_cursor in explored_cursors:
            print("Reached the end of reviews.")
            break
        
        explored_cursors.add(new_cursor)
        params["cursor"] = new_cursor
        
        # Sleep to avoid rate limiting
        time.sleep(1)
    
    return reviews

# Fetch and save reviews to CSV
reviews = fetch_reviews()
df = pd.DataFrame(reviews)
# Double-check: remove rows with NaN or empty strings in Text/Label
df = df.dropna(subset=["Text", "Label"])  # Remove NaN
df = df[df["Text"].str.strip() != ""]     # Remove empty strings
df.to_csv("stalker_reviews.csv", index=False)
print(f"Saved {len(df)} reviews to stalker_reviews.csv")