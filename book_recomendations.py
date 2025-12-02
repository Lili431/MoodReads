import random
import pandas as pd
class Book:#Made a Book class as a requirement for the project
    def __init__(self, title, author, genre, rating, pages, description, image=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.pages = pages
        self.description = description
        self.image = image
    def to_dict(self):#Convert book object to dictionary(I've learned that flask prefers dictionaries).
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
            "pages": self.pages,
            "description": self.description,
            "image": self.image,
        }
def load_books(csv_path):#Loads books from a CSV into a DataFrame using pandas
    df = pd.read_csv(csv_path)
    df = df.rename(columns={"average_rating": "rating","thumbnail": "image"})#Rename columns to match our code to make life easier
    #Handle missing values
    df["genre"] = df["genre"].fillna("Unknown")#books with no genres will be marked unknown to show a value
    df["rating"] = df["rating"].replace("No rating", "None").astype(str)#books with no ratings will be marked as None for the output to show the user
    df["pages"] = df["pages"].fillna("N/A")#
    df["description"] = df["description"].fillna("No description available")
    return df
MOOD_GENRE_MAP = { #Connects a mood (like "happy") to specific genres
    "happy": ["romance", "comedy", "feel-good"],
    "sad": ["inspirational", "self-help"],
    "cozy": ["fiction", "classics", "romance"],
    "adventurous": ["fantasy", "sci-fi", "thriller"],
    "mysterious": ["mystery", "thriller", "crime"],
    "thoughtful": ["non-fiction", "philosophy", "literary criticism"],
    "sleepy": ["Literary Criticism", "Science fiction", "Statistics"],
    "nuetral": ["philosophy", "sci-fi", "fiction"]
    #I may add more onto this dictionary to have more options availiable
}
def get_recommendations(mood, df, num_books=5):#Get book recommendations based on current mood, up to 5 books will be recommended.
    mood = mood.lower()#I have this here to make the user input in all lowercase so it matches the keys in the Mood dictionary
    genres = MOOD_GENRE_MAP.get(mood, [mood])# Look up the mood in our mood dictionary to get the list of genres. If the mood isn't found, just search for the mood word itself.
    filtered = df[df["genre"].str.lower().isin(genres)]#Go through the Books.csv file and grab only the matching books
    #Worst case but if no books match, just pick random ones to give a user some book to try out
    if filtered.empty:
        filtered = df.sample(min(num_books, len(df)))
    else:
        filtered = filtered.sample(frac=1).head(num_books)#however, shuffle them and pick the top 5
    books = [#Convert DataFrame rows to Book objects
        Book(row["title"],row["author"],row["genre"],row["rating"],row["pages"],row["description"],row.get("image", None),)
        for x, row in filtered.iterrows()
    ]
    random.shuffle(books)#use ramdom import to suffle books
    return books

if __name__ == "__main__":
    # Testsing code out to make sure it works!
    df = load_books("/Users/lilianatrejo/Data_Science_Project/Books.csv")
    user_mood = input("Enter your mood: ")#user types a mood so they can get a book recommendation
    recs = get_recommendations(user_mood, df)
    print(f"\nBook recommendations for your mood '{user_mood}':\n")
    for book in recs:
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Genre: {book.genre}")
        print(f"Rating: {book.rating}")
        print(f"Pages: {book.pages}")
        print(f"Description: {book.description}\n")
