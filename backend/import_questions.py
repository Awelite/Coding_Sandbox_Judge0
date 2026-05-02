import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="ai_interviewer"
)

cursor = conn.cursor()

# Load JSON
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

for q in questions:

    # Insert problem
    cursor.execute("""
        INSERT INTO coding_problems
        (slug, title, difficulty, topic, description,
         constraints_text, examples, tags, companies, starter_code)

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        q["slug"],
        q["title"],
        q["difficulty"],
        q["topic"],
        q["description"],
        q["constraints"],
        q["examples"],
        q["tags"],
        q["companies"],
        json.dumps(q["starter_code"])
    ))

    problem_id = cursor.lastrowid

    # Insert test cases
    for tc in q["test_cases"]:
        cursor.execute("""
            INSERT INTO test_cases
            (problem_id, input_data, expected_output, is_hidden)

            VALUES (%s,%s,%s,%s)
        """, (
            problem_id,
            tc["input"],
            tc["output"],
            tc["hidden"]
        ))

conn.commit()

print("Questions imported successfully!")