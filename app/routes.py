import sqlite3
from flask import Blueprint, render_template, request, json
from .db import get_db_connection, get_sentiment_db_connection

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

# 관광지, 감성에 따라 조회 수행행
def get_data_from(table, sentiment):
    conn = sqlite3.connect(f'bigram_{table}.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM bigram_{table} WHERE word1 = \"{sentiment}\" OR word2 = \"{sentiment}\"")
    rows = cursor.fetchall()
    conn.close()
    return rows

# 계명한학촌
@main.route('/sentiment_kmy')
def kmy_sentiment():
    return render_template('sentiment_계명한학촌.html')

@main.route('/sentiment_kmy/detail')
def kmy_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 고모역
@main.route('/sentiment_gomostn')
def gomostn_sentiment():
    return render_template('sentiment_고모역.html')

@main.route('/sentiment_gomostn/detail')
def gomostn_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 대구아쿠아리움
@main.route('/sentiment_aqua')
def aqua_sentiment():
    return render_template('sentiment_대구아쿠아리움.html')

@main.route('/sentiment_aqua/detail')
def aqua_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 대명유수지
@main.route('/sentiment_yusu')
def yusu_sentiment():
    return render_template('sentiment_대명유수지.html')

@main.route('/sentiment_yusu/detail')
def yusu_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 도동서원
@main.route('/sentiment_dodong')
def dodong_sentiment():
    return render_template('sentiment_도동서원.html')

@main.route('/sentiment_dodong/detail')
def dodong_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 사문진
@main.route('/sentiment_samunjin')
def samunjin_sentiment():
    return render_template('sentiment_사문진.html')

@main.route('/sentiment_samunjin/detail')
def samunjin_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 송해공원
@main.route('/sentiment_songhae')
def songhae_sentiment():
    return render_template('sentiment_송해공원.html')

@main.route('/sentiment_songhae/detail')
def songhae_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 신전뮤지엄
@main.route('/sentiment_sinjeon')
def sinjeon_sentiment():
    return render_template('sentiment_신전뮤지엄.html')

@main.route('/sentiment_sinjeon/detail')
def sinjeon_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 정호승문학관
@main.route('/sentiment_jeonghoseung')
def jeonghoseung_sentiment():
    return render_template('sentiment_정호승문학관.html')

@main.route('/sentiment_jeonghoseung/detail')
def jeonghoseung_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)

# 진달래군락지
@main.route('/sentiment_jindallae')
def jindallae_sentiment():
    return render_template('sentiment_진달래군락지.html')

@main.route('/sentiment_jindallae/detail')
def jindallae_sentiment_detail():
    table = request.args.get('table', '')
    sentiment = request.args.get('sentiment', '')
    data = get_data_from(table, sentiment)
    return render_template('sentiment_detail.html', results=data, table=table, sentiment=sentiment)