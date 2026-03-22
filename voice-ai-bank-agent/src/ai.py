"""
ai.py — Context-grounded AI engine for Armenian banking assistant.
Loads scraped bank data and injects it as strict context into the LLM prompt.
The model is instructed to ONLY answer from this data.
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def load_data(path=None):
    if path is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "data", "bank_data.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_context(data: list) -> str:
    blocks = []
    for entry in data:
        blocks.append(
            f"Բանկ: {entry['bank']}\n"
            f"Ոլորտ: {entry['topic']}\n"
            f"Տեղեկություն: {entry['content']}\n"
            f"Աղբյուր: {entry['source']}"
        )
    return "\n\n---\n\n".join(blocks)


def build_system_prompt(context: str) -> str:
    return f"""Դու հայկական բանկային AI օգնական ես։

ԽԻՍՏ ԿԱՆՈՆՆԵՐ

Պատասխանիր բացառապես տրամադրված բանկային տվյալների հիման վրա։
Թույլատրելի թեմաներ՝ վարկեր, ավանդներ, մասնաճյուղեր։
Եթե հարցը չի վերաբերում այս թեմաներին, ասա՝
«Ես չեմ կարող պատասխանել այդ հարցին։ Կարող եմ օգնել միայն վարկերի, ավանդների և մասնաճյուղերի վերաբերյալ հարցերում»։
Մի հորինիր, մի ենթադրիր, մի օգտագործիր արտաքին գիտելիք։
Պատասխանիր հայերեն, կարճ և հստակ։

ԲԱՆԿԱՅԻՆ ՏՎՅԱԼՆԵՐ
{context}
"""


def ask_ai(user_input: str, data: list) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    context = build_context(data)
    system_prompt = build_system_prompt(context)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    )

    return response.choices[0].message.content.strip()ssage.content.strip()
