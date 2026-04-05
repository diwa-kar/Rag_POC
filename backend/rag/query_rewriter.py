from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def rewrite_query(query, history):
    history_text = ""
    for msg in history:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
Rewrite the query into a standalone question.

Chat History:
{history_text}

User Query:
{query}

Rewritten Query:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )



    return response.choices[0].message.content.strip()