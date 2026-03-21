import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def load_data(path="data/bank_data.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_context(data):
    return "\n\n".join([
        f"Bank: {d['bank']}\nTopic: {d['topic']}\nContent: {d['content']}"
        for d in data
    ])


def ask_ai(user_input, data):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    context = build_context(data)

    system_prompt = """
You are an Armenian banking assistant.

STRICT RULES:
- Answer ONLY using the provided context
- Allowed topics: credits, deposits, branch locations
- If question is outside → say: "Ես չեմ կարող պատասխանել այդ հարցին"
- Do NOT use external knowledge
- Answer in Armenian
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt + context},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()