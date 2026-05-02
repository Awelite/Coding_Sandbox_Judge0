from datetime import datetime
from services.ai_review import generate_ai_review
from fastapi import APIRouter
import mysql.connector
import json
import requests
import os
import time
import base64
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/coding", tags=["Coding"])

# ---------------- DB CONNECTION ---------------- #

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),  # safer
        database="ai_interviewer"
    )

# ---------------- GET PROBLEM ---------------- #

@router.get("/problem/{slug}")
def get_problem(slug: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            starter_code,
            difficulty,
            topic,
            examples,
            constraints_text AS constraints,
            tags,
            companies
        FROM coding_problems
        WHERE slug=%s
        """,
        (slug,)
    )

    problem = cursor.fetchone()

    cursor.close()
    conn.close()

    if problem:
        problem["starter_code"] = json.loads(problem["starter_code"])
        return problem

    return {"error": "Problem not found"}


# ===============================
# 🔥 RUN CODE
# ===============================

LANGUAGE_MAP = {
    "python": 71,
    "cpp": 54
}

# ✅ Default test inputs per problem (used if frontend doesn't send stdin)
PROBLEM_TEST_INPUTS = {
    "two_sum": "2 7 11 15\n9",
}

@router.post("/run")
def run_code(payload: dict):
    try:
        source_code = payload.get("code")
        language = payload.get("language")
        problem_slug = payload.get("problem_slug", "")

        language_id = LANGUAGE_MAP.get(language)

        if not language_id:
            return {"output": "Unsupported language"}

        # ✅ Use stdin from frontend, fallback to problem's default test input
        stdin_data = payload.get("stdin") or PROBLEM_TEST_INPUTS.get(problem_slug, "")
        print(f"[DEBUG] problem_slug={problem_slug!r} | stdin_data={stdin_data!r}")

        judge0_url = "http://localhost:2358/submissions?base64_encoded=true&wait=true"

        response = requests.post(
            judge0_url,
            json={
                "source_code": base64.b64encode(source_code.encode()).decode(),
                "language_id": language_id,
                "stdin": base64.b64encode(stdin_data.encode()).decode()
            },
            timeout=30
        )

        result = response.json()

        stdout = result.get("stdout")
        stderr = result.get("stderr")
        compile_output = result.get("compile_output")
        message = result.get("message")

        # ✅ Decode stdout
        if stdout:
            return {
                "output": base64.b64decode(stdout).decode()
            }

        # ✅ Decode stderr
        if stderr:
            return {
                "output": base64.b64decode(stderr).decode()
            }

        # ✅ Decode compile errors
        if compile_output:
            return {
                "output": base64.b64decode(compile_output).decode()
            }

        # ✅ Decode Judge0 system message
        if message:
            try:
                decoded = base64.b64decode(message).decode()
                return {"output": decoded}
            except:
                return {"output": message}

        return {"output": "No Output"}

    except Exception as e:
        return {"output": f"Execution error: {str(e)}"}


@router.post("/submit")
def submit_solution(payload: dict):

    try:
        code = payload.get("code")
        language = payload.get("language")
        slug = payload.get("problem_slug")

        language_id = LANGUAGE_MAP.get(language)

        if not language_id:
            return {"error": "Unsupported language"}

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # =========================
        # GET PROBLEM
        # =========================

        cursor.execute(
            """
            SELECT id, title, description
            FROM coding_problems
            WHERE slug=%s
            """,
            (slug,)
        )

        problem = cursor.fetchone()

        if not problem:
            return {"error": "Problem not found"}

        problem_id = problem["id"]

        # =========================
        # GET TEST CASES
        # =========================

        cursor.execute(
            """
            SELECT input_data, expected_output, is_hidden
            FROM test_cases
            WHERE problem_id=%s
            """,
            (problem_id,)
        )

        test_cases = cursor.fetchall()

        results = []
        passed = 0

        # =========================
        # RUN EACH TEST
        # =========================

        for test in test_cases:

            stdin = test["input_data"]

            response = requests.post(
                "http://localhost:2358/submissions?base64_encoded=false&wait=true",
                json={
                    "source_code": code,
                    "language_id": language_id,
                    "stdin": stdin
                },
                timeout=20
            )

            # SAFE JSON PARSE
            try:
                result = response.json()
            except Exception:
                result = {
                    "stderr": "Judge0 failed to respond properly"
                }

            status = result.get("status", {})
            status_desc = status.get("description", "Unknown Error")

            stdout = result.get("stdout")
            stderr = result.get("stderr")
            compile_output = result.get("compile_output")

            actual_output = ""

            # =========================
            # HANDLE JUDGE0 VERDICTS
            # =========================

            if stdout:
                actual_output = stdout.strip()

            elif stderr:
                actual_output = stderr.strip()

            elif compile_output:
                actual_output = compile_output.strip()

            expected_output = test["expected_output"].strip()

            # =========================
            # DETECT PROFESSIONAL VERDICT
            # =========================

            if status_desc == "Accepted":

                if actual_output == expected_output:
                    test_verdict = "Accepted"
                    is_passed = True
                    passed += 1

                else:
                    test_verdict = "Wrong Answer"
                    is_passed = False

            elif "Compilation Error" in status_desc:
                test_verdict = "Compilation Error"
                is_passed = False

            elif "Runtime Error" in status_desc:
                test_verdict = "Runtime Error"
                is_passed = False

            elif "Time Limit Exceeded" in status_desc:
                test_verdict = "Time Limit Exceeded"
                is_passed = False

            elif "Memory Limit Exceeded" in status_desc:
                test_verdict = "Memory Limit Exceeded"
                is_passed = False

            else:
                test_verdict = status_desc
                is_passed = False

            # =========================
            # ONLY SHOW PUBLIC TESTS
            # =========================

            if test["is_hidden"] == 0:

                results.append({
                    "input": stdin,
                    "expected": expected_output,
                    "actual": actual_output,
                    "passed": is_passed,
                    "verdict": test_verdict
                })

        total = len(test_cases)

        score = round((passed / total) * 100, 2)

        cursor.close()
        conn.close()

        # =========================
        # PROFESSIONAL VERDICT
        # =========================

        if passed == total:
            verdict = "Accepted"

        elif passed == 0:

            first_failed = results[0]["verdict"] if results else "Wrong Answer"

            if first_failed == "Compilation Error":
                verdict = "Compilation Error"

            elif first_failed == "Runtime Error":
                verdict = "Runtime Error"

            elif first_failed == "Time Limit Exceeded":
                verdict = "Time Limit Exceeded"

            elif first_failed == "Memory Limit Exceeded":
                verdict = "Memory Limit Exceeded"

            else:
                verdict = "Wrong Answer"

        else:
            verdict = "Partially Accepted"

        ai_review = generate_ai_review(
            problem["description"],
            code,
            verdict
        )

        return {
            "verdict": verdict,
            "passed_tests": passed,
            "total_tests": total,
            "score": score,
            "results": results,
            "ai_review": ai_review
        }

    except Exception as e:
        return {"error": str(e)}

# ---------------- SAVE SUBMISSION ---------------- #

@router.post("/save-submission")
def save_submission(payload: dict):

    conn = get_db()
    cursor = conn.cursor()

    problem_id = payload.get("problem_id")
    language = payload.get("language")
    code = payload.get("code")
    verdict = payload.get("verdict")

    cursor.execute("""
        INSERT INTO submissions
        (problem_id, language, code, verdict)

        VALUES (%s, %s, %s, %s)
    """, (
        problem_id,
        language,
        code,
        verdict
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Submission saved"
    }

# ---------------- GET SOLVED PROBLEMS ---------------- #

@router.get("/solved-problems")
def solved_problems():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DISTINCT problem_id
        FROM submissions
        WHERE verdict='Accepted'
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    solved_ids = [row["problem_id"] for row in rows]

    return solved_ids

# ---------------- GET ALL PROBLEMS ---------------- #

@router.get("/problems")
def get_problems(
    difficulty: str = None,
    topic: str = None,
    search: str = None
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, slug, title, difficulty, topic
        FROM coding_problems
        WHERE 1=1
    """

    values = []

    # Difficulty filter
    if difficulty and difficulty != "all":
        query += " AND difficulty=%s"
        values.append(difficulty)

    # Topic filter
    if topic and topic != "all":
        query += " AND topic=%s"
        values.append(topic)

    # Search filter
    if search:
        query += " AND title LIKE %s"
        values.append(f"%{search}%")

    query += " ORDER BY id ASC"

    cursor.execute(query, values)

    problems = cursor.fetchall()

    cursor.close()
    conn.close()

    return problems
