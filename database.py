import sqlite3
from collections import Counter

DB_NAME = "cine.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            genre TEXT,
            rating INTEGER,
            status TEXT,
            notes TEXT,
            poster TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_movie(title, genre, rating, status, notes, poster):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO movies (title, genre, rating, status, notes, poster) VALUES (?, ?, ?, ?, ?, ?)",
              (title, genre, rating, status, notes, poster))
    conn.commit()
    conn.close()

def get_all_movies():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = c.fetchall()
    conn.close()
    return movies

def delete_all_movies():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM movies")
    conn.commit()
    conn.close()

def delete_movie_by_id(movie_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()

def init_recommendation_data():
    data = [
        ("Inception", "Sci-Fi"),
        ("The Matrix", "Sci-Fi"),
        ("Interstellar", "Sci-Fi"),
        ("The Dark Knight", "Aksi"),
        ("Joker", "Drama"),
        ("Avengers: Endgame", "Aksi"),
        ("The Godfather", "Drama"),
        ("Parasite", "Drama"),
        ("Get Out", "Horor"),
        ("The Conjuring", "Horor"),
        ("The Hangover", "Komedi"),
        ("Forrest Gump", "Drama"),
        ("Titanic", "Drama"),
        ("The Shawshank Redemption", "Drama"),
        ("La La Land", "Fantasi")
    ]

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS movie_references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            genre TEXT
        )
    ''')
    c.execute("SELECT COUNT(*) FROM movie_references")
    if c.fetchone()[0] == 0:  
        c.executemany("INSERT INTO movie_references (title, genre) VALUES (?, ?)", data)
    conn.commit()
    conn.close()

def get_recommendations(genre, exclude_title=None, limit=3):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if exclude_title:
        c.execute("SELECT title FROM movie_references WHERE genre = ? AND title != ? LIMIT ?", (genre, exclude_title, limit))
    else:
        c.execute("SELECT title FROM movie_references WHERE genre = ? LIMIT ?", (genre, limit))
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

def get_recommendation_based_on_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT genre FROM movies WHERE status='Watched'")
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()

    if len(genres) < 5:
        return None

    genre_count = Counter(genres)
    top_genre = genre_count.most_common(1)[0][0]

    genre_recommendation = {
        "Aksi": ["John Wick", "Mad Max: Fury Road"],
        "Komedi": ["The Hangover", "Superbad"],
        "Drama": ["The Pursuit of Happyness", "Forrest Gump"],
        "Fantasi": ["Harry Potter", "The Hobbit"],
        "Horor": ["The Conjuring", "Insidious"],
        "Sci-Fi": ["Inception", "Interstellar"],
        "Thriller": ["Gone Girl", "Se7en"]
    }

    recommended_titles = genre_recommendation.get(top_genre, ["No recommendation"])
    return f"Tampaknya kamu sangat menyukai genre {top_genre}. Kami merekomendasikan: {', '.join(recommended_titles)}"
