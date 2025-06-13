import pandas as pd
from sqlalchemy import create_engine, text
from db.init import SessionLocal
from db.models import Answer, User

def export_answers_to_excel(output_path="survey_answers.xlsx"):
    session = SessionLocal()

    # Get latest answers per question per user (using max version)
    query = text("""
        SELECT
            a.user_id,
            u.telegram_id,
            u.username,
            a.question,
            a.answer,
            a.version,
            a.timestamp
        FROM answers a
        JOIN (
            SELECT user_id, question, MAX(version) AS max_version
            FROM answers
            GROUP BY user_id, question
        ) latest
        ON a.user_id = latest.user_id
        AND a.question = latest.question
        AND a.version = latest.max_version
        JOIN users u ON u.id = a.user_id
        ORDER BY a.user_id, a.timestamp
    """)

    result = session.execute(query)
    rows = result.fetchall()

    # Convert to pandas DataFrame
    df = pd.DataFrame(rows, columns=["user_id", "telegram_id", "username", "question", "answer", "version", "timestamp"])

    # Pivot: One row per user, one column per question
    df_pivot = df.pivot_table(index=["telegram_id", "username"], columns="question", values="answer", aggfunc="first").reset_index()

    # Save to Excel
    df_pivot.to_excel(output_path, index=False)
    print(f"✅ Exported to {output_path}")

    session.close()

if __name__ == "__main__":
    export_answers_to_excel()
