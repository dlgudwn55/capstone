import pandas as pd
import sqlite3

df = pd.read_excel('tour_keywords.xlsx')

# SQLite 데이터베이스 연결 (없으면 생성됨)
conn = sqlite3.connect('tour.db')

# DataFrame을 'tour_contents' 테이블로 저장
df.to_sql('tour_contents', conn, if_exists='replace', index=False)

conn.close()
print("엑셀 데이터를 SQLite 데이터베이스로 변환 완료.")
