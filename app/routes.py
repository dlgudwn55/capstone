from flask import Blueprint, render_template, request, json
from .db import get_db_connection

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search')
def search():
    rows = []

    query = request.args.get('q', '')
    keywords = query.split()

    if len(keywords) == 1:
        where_clause = "keyword1 LIKE ? OR keyword2 LIKE ? OR keyword3 LIKE ?"
        params = [*keywords[:]] * 3
    elif len(keywords) == 2:
        where_clause = "keyword1 LIKE ? AND keyword2 LIKE ? OR \
            keyword1 LIKE ? AND keyword3 LIKE ? OR \
            keyword2 LIKE ? AND keyword1 LIKE ? OR \
            keyword2 LIKE ? AND keyword3 LIKE ? OR \
            keyword3 LIKE ? AND keyword1 LIKE ? OR \
            keyword3 LIKE ? AND keyword2 LIKE ?"
        params = [*keywords[:]] * 6
    else:
        where_clause = "keyword1 LIKE ? AND keyword2 LIKE ? AND keyword3 LIKE ? OR \
            keyword1 LIKE ? AND keyword3 LIKE ? AND keyword2 LIKE ? OR \
            keyword2 LIKE ? AND keyword1 LIKE ? AND keyword3 LIKE ? OR \
            keyword2 LIKE ? AND keyword3 LIKE ? AND keyword1 LIKE ? OR \
            keyword3 LIKE ? AND keyword1 LIKE ? AND keyword2 LIKE ? OR \
            keyword3 LIKE ? AND keyword2 LIKE ? AND keyword2 LIKE ?"
        params = [*keywords[:]] * 6
    print(params)
    
    conn = get_db_connection()
    cur = conn.cursor()

    # where_clause = " OR ".join(["keyword1 LIKE ? OR keyword2 LIKE ? OR keyword3 LIKE ?" for _ in keywords])
    # print(where_clause)
    # params = []
    # for kw in keywords:
    #     params.extend([kw, kw, kw])
    #     conn = get_db_connection()
    #     cur = conn.cursor()
    # print(params)
    # print([f'{kw}' for kw in params])

    if query:
        cur.execute(f"""
            SELECT site, keyword1, keyword2, keyword3, MAX(frequency) as frequency, blog_link, blog_title, blog_id
            FROM tour_contents_v3
            WHERE {where_clause}
            GROUP BY blog_link
            ORDER BY frequency DESC
        """, [f'%{kw}%' for kw in params])
        print("SQL executed")
        rows = cur.fetchall()
        count = len(rows)
    return render_template('search.html', results=rows, count=count, query=query)


@main.route('/site')
def site():
    # 여행지 클릭하면 해당 여행지 관련 블로그 포스트 보기로 제목에 하이퍼링크가 된 것들이 랜덤으로 10개 표시
    rows = []

    query = request.args.get('q', '')

    conn = get_db_connection()
    cur = conn.cursor()

    if query:
        cur.execute(f"""
            SELECT DISTINCT blog_title, blog_link
            FROM tour_contents_v3
            WHERE site = ?
            ORDER BY RANDOM()
            LIMIT 10
        """, (query,))
        print("SQL executed")
        rows = cur.fetchall()
    return render_template('site.html', results=rows, query=query)
