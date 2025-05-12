from .db import get_db_connection

def get_trigrams_by_keyword(keyword):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT keyword1, keyword2, keyword3, frequency, link
        FROM trigrams
        WHERE keyword1 = ? OR keyword2 = ? OR keyword3 = ?
        ORDER BY frequency DESC
        LIMIT 50
    """, (keyword, keyword, keyword))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_blog_by_id(blog_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogs WHERE id = ?", (blog_id,))
    blog = cur.fetchone()
    conn.close()
    return blog
