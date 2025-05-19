import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tour_v3.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_sentiment_db_connection(site):
    conn = sqlite3.connect(f'bigram_{site}.db')
    conn.row_factory = sqlite3.Row
    return conn
