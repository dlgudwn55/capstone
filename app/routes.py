from flask import Blueprint, render_template, request, json
from .db import get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return  render_template('index.html')

@main.route('/search')
def search():
    rows = []

    query = request.args.get('q', '')
    keywords = query.split()

    where_clause = " OR ".join(["keyword1 LIKE ? OR keyword2 LIKE ? OR keyword3 LIKE ?" for _ in keywords])
    print(where_clause)
    params = []
    for kw in keywords:
        params.extend([kw, kw, kw])
        conn = get_db_connection()
        cur = conn.cursor()
    print(params)
    print([f'{kw}' for kw in params])

    if query:
        cur.execute(f"""
            SELECT site, keyword1, keyword2, keyword3, MAX(frequency) as frequency, blog_link, blog_title, blog_id
            FROM tour_contents_v2
            WHERE {where_clause}
            GROUP BY blog_link
            ORDER BY frequency DESC
        """, [f'%{kw}%' for kw in params])
        print("SQL executed")
        rows = cur.fetchall()
        count = len(rows)
    return render_template('search.html', results=rows, count=count, query=query)
    # return json.dumps(rows)
    # return json.dumps([dict(row) for row in rows], ensure_ascii=False)
