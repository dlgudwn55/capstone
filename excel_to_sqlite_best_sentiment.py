import pandas as pd
import sqlite3

df = pd.read_excel('정규화된_감성어_빈도_데이터_20.xlsx')

# SQLite 데이터베이스 연결 (없으면 생성됨)
conn = sqlite3.connect('best_sentiment_20.db')

# DataFrame을 'tour_contents' 테이블로 저장
df.to_sql('best_sentiment_20', conn, if_exists='replace', index=False)

conn.close()
print("csv 데이터를 SQLite 데이터베이스로 변환 완료.")
