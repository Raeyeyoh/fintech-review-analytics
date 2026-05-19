import pandas as pd
import psycopg2

df = pd.read_csv("data/sentiment_analysis_results.csv")

conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="ADMIN321"
)

cur = conn.cursor()

bank_mapping = {
    "CBE": 1,
    "BOA": 2,
    "Dashen": 3
}

# Insert rows
for index, row in df.iterrows():

    bank_id = bank_mapping.get(row["bank"])

    cur.execute("""
        INSERT INTO reviews (
            bank_id,
            review_text,
            rating,
            review_date,
            sentiment_label,
            sentiment_score,
            identified_theme,
            source
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        bank_id,
        row["review"],
        row["rating"],
        row["date"],
        row["sentiment_label"],
        row["sentiment_score"],
        row["identified_theme"],
        row["source"]
    ))

conn.commit()

cur.close()
conn.close()

print("Data inserted successfully!")
