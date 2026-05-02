from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_ai_review(problem, code, verdict):
    try:
        prompt = f"""
You are a senior technical interviewer.

Analyze this coding interview submission.

Problem:
{problem}

Verdict:
{verdict}

Candidate Code:
{code}

Provide:

1. Correctness analysis
2. Time complexity
3. Space complexity
4. Optimization suggestions
5. Code quality review
6. Interview-style feedback

Keep response professional and concise.
"""

        completion = client.chat.completions.create(
            model="nvidia/nemotron-nano-12b-v2-vl:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f"[AI REVIEW ERROR]: {e}")
        return f"AI review unavailable at this time. Error: {str(e)}"