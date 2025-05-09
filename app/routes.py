from flask import Blueprint, render_template, request
from .db import get_db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    query = request.args.get('q', '')
    conn = get_db()
    cur = conn.cursor()
    rows = []
    if query:
        cur.execute("""
            SELECT keyword1, keyword2, keyword3, link
            FROM tour_contents
            WHERE keyword1 = ? OR keyword2 = ? OR keyword3 = ? OR link LIKE ?
        """, (query, query, query, f'%{query}%'))
        rows = cur.fetchall()
    return render_template('index.html', results=rows, query=query)
