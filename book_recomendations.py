import random
import pandas as pd

# my Book class
class Book:
    def __init__(self, title, author, genre, rating, pages, description, image=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.pages = pages
        self.description = description
        self.image = image

    def to_dict(self):
        """Convert book object to dictionary (for rendering in Flask)."""
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
            "pages": self.pages,
            "description": self.description,
            "image": self.image,
        }

#load csv dataset
def load_books(csv_path):
    """Loads books from a CSV into a cleaned DataFrame."""
    df = pd.read_csv(csv_path)

    # Rename columns to match our code
    df = df.rename(columns={
        "average_rating": "rating",
        "thumbnail": "image"
    })

    # Handle missing values
    df["genre"] = df["genre"].fillna("Unknown")
    df["rating"] = df["rating"].replace("No rating", 0).astype(str)
    df["pages"] = df["pages"].fillna("N/A")
    df["description"] = df["description"].fillna("No description available")

    return df

#Mood to genre mapping
MOOD_GENRE_MAP = {
    "happy": ["romance", "comedy", "feel-good"],
    "sad": ["inspirational", "self-help"],
    "cozy": ["fiction", "classics", "romance"],
    "adventurous": ["fantasy", "sci-fi", "thriller"],
    "mysterious": ["mystery", "thriller", "crime"],
    "thoughtful": ["non-fiction", "philosophy", "literary criticism"],
}

#Get recommendations based on mood
def get_recommendations(mood, df, num_books=5):
    mood = mood.lower()
    genres = MOOD_GENRE_MAP.get(mood, [mood])
    filtered = df[df["genre"].str.lower().isin(genres)]

    if filtered.empty:
        filtered = df.sample(min(num_books, len(df)))
    else:
        filtered = filtered.sample(frac=1).head(num_books)

    # Convert DataFrame rows to Book objects
    books = [
        Book(
            row["title"],
            row["author"],
            row["genre"],
            row["rating"],
            row["pages"],
            row["description"],
            row.get("image", None),
        )
        for _, row in filtered.iterrows()
    ]

    random.shuffle(books)
    return books

if __name__ == "__main__":
    df = load_books("/Users/lilianatrejo/Data_Science_Project/Books.csv")
    user_mood = input("Enter your mood: ")  #user types a mood
    recs = get_recommendations(user_mood, df)

    print(f"\nBook recommendations for your mood '{user_mood}':\n")
    for book in recs:
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Genre: {book.genre}")
        print(f"Rating: {book.rating}")
        print(f"Pages: {book.pages}")
        print(f"Description: {book.description}\n")
