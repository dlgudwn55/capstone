import pandas as pd
import sqlite3

sites = ["계명한학촌", "고모역", "대구아쿠아리움", "대명유수지", "도동서원", "사문진", "송해공원", "신전뮤지엄", "정호승문학관", "진달래군락지"]

for site in sites:
    df = pd.read_excel(f'./Bigram/bigram_{site}.xlsx')

    # SQLite 데이터베이스 연결 (없으면 생성됨)
    conn = sqlite3.connect(f'bigram_{site}.db')

    # DataFrame을 'tour_contents' 테이블로 저장
    df.to_sql(f'bigram_{site}', conn, if_exists='replace', index=False)

    conn.close()

    print(f"{site} 엑셀 데이터를 SQLite 데이터베이스로 변환 완료.")
