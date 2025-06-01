import sqlite3
from datetime import datetime, timedelta
from .models import Item

class SpacedRepetitionDB:
    def __init__(self, db_path='learning_items.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                next_review TIMESTAMP,
                review_count INTEGER DEFAULT 0,
                ease_factor REAL DEFAULT 2.5
            )
        ''')
        self.conn.commit()

    def add_item(self, content):
        next_review = datetime.now() + timedelta(days=1)
        self.cursor.execute('''
            INSERT INTO items (content, next_review)
            VALUES (?, ?)
        ''', (content, next_review))
        self.conn.commit()

    def get_due_item(self):
        self.cursor.execute('''
            SELECT id, content, created_at, next_review, review_count, ease_factor FROM items 
            WHERE next_review <= datetime('now')
            ORDER BY next_review ASC
            LIMIT 1
        ''')
        row = self.cursor.fetchone()
        if row:
            return Item(*row)
        return None

    def update_item_review(self, item_id, review_count, ease_factor, interval):
        next_review = datetime.now() + timedelta(days=interval)
        self.cursor.execute('''
            UPDATE items
            SET next_review = ?, review_count = ?, ease_factor = ?
            WHERE id = ?
        ''', (next_review, review_count, ease_factor, item_id))
        self.conn.commit()

    def get_stats(self):
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total_items,
                SUM(CASE WHEN next_review <= datetime('now') THEN 1 ELSE 0 END) as due_items,
                AVG(review_count) as avg_reviews
            FROM items
        ''')
        stats = self.cursor.fetchone()
        avg_reviews = stats[2] if stats[2] is not None else 0.0
        return stats[0], stats[1], avg_reviews

    def close(self):
        self.conn.close()

# Spaced repetition algorithm

def calculate_next_interval_and_ease(review_count, ease_factor, rating):
    if rating == "Easy":
        interval = max(1, int(ease_factor * (review_count + 1)))
        ease_factor = min(2.5, ease_factor + 0.1)
    elif rating == "Good":
        interval = max(1, int(ease_factor * review_count))
        ease_factor = max(1.3, ease_factor - 0.1)
    else:  # Hard
        interval = 1
        ease_factor = max(1.3, ease_factor - 0.2)
    return interval, ease_factor 