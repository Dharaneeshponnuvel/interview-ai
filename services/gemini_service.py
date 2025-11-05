import os
import json
import requests
from config import GEMINI_API_KEY, GEMINI_URL, DEFAULT_NUM_QUESTIONS, MAX_RESUME_CHARS

def call_gemini(prompt: str) -> str:
    """Generic function to send a prompt to Gemini API."""
    headers = {"Content-Type": "application/json"}
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code != 200:
        raise Exception(f"Gemini Error: {res.status_code} {res.text}")

    data = res.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return text


def build_question_prompt(job_title, resume_text, num=DEFAULT_NUM_QUESTIONS):
    resume = resume_text[:MAX_RESUME_CHARS]
    return f"""
You are an expert interviewer.
Generate {num} JSON interview questions for the role: {job_title}.

Return STRICT JSON:
{{
  "questions": [
    {{"id":"q1","text":"...","type":"technical|behavioral|open","focus":"...","hints":"..."}}
  ],
  "system_tip": "one line tip"
}}

Resume:
{resume}
"""


def generate_questions(job_title, resume_text, num=DEFAULT_NUM_QUESTIONS):
    prompt = build_question_prompt(job_title, resume_text, num)
    response = call_gemini(prompt)
    try:
        start, end = response.find("{"), response.rfind("}") + 1
        parsed = json.loads(response[start:end])
        return parsed
    except Exception:
        # fallback
        return {
            "questions": [
                {
                    "id": "q1",
                    "text": "Tell me about a challenging project you mentioned in your resume.",
                    "type": "open",
                    "focus": "experience",
                    "hints": "Context, action, result"
                }
            ],
            "system_tip": "Be concise and specific."
        }


def build_evaluate_prompt(job_title, resume_text, question, answer):
    resume = resume_text[:MAX_RESUME_CHARS]
    return f"""
Evaluate the candidate's answer based on resume and role.
Return STRICT JSON:
{{
  "score": 0-100,
  "strengths": ["..."],
  "improvements": ["..."],
  "sample_response": "...",
  "follow_up_question": "..."
}}

Role: {job_title}
Resume: {resume}
Question: {question}
Answer: {answer}
"""


def evaluate_answer(job_title, resume_text, question, answer):
    prompt = build_evaluate_prompt(job_title, resume_text, question, answer)
    response = call_gemini(prompt)
    try:
        start, end = response.find("{"), response.rfind("}") + 1
        return json.loads(response[start:end])
    except Exception:
        return {
            "score": 65,
            "strengths": ["Good clarity"],
            "improvements": ["Add specific examples."],
            "sample_response": "A strong response clearly explains context, action, and measurable result.",
            "follow_up_question": "Can you elaborate on how you measured success?"
        }
