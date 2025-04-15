import os
import requests
from dotenv import load_dotenv

load_dotenv()

def call_openrouter_arli(prompt, model="mistralai/mistral-7b-instruct"):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    url = "https://openrouter.ai/api/v1/chat/completions"
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def write_email(name: str, recipient_info: str, jd_text: str, resume_summary: str = "") -> str:
    prompt = f"""
You are a helpful job outreach assistant. Generate a personalized cold email to {name}, based on the following context:

=== Recipient Info ===
{recipient_info}

=== Job Description (AI & Backend Developer) ===
{jd_text}

=== My Summary ===
{resume_summary}

Make it sound human, concise (max 150 words), polite, and a bit enthusiastic. Do NOT sound robotic or generic.

Return only the email body. Start with "Hi <recipient name>" if possible.
"""
    return call_openrouter_arli(prompt)

# Example usage
if __name__ == "__main__":
    email = write_email(
        name="Ananya",
        recipient_info="Hiring Manager at AI Startup focused on NLP and Chatbots",
        jd_text="Looking for a backend developer with experience in Python, FastAPI, and AI toolchains like LangChain. Bonus if familiar with LLM integration.",
        resume_summary="Backend developer with 2+ years experience building scalable APIs using FastAPI and integrating LLMs using LangChain and OpenAI."
    )
    print(email)
