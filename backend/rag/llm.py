from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()  # loads variables from .env

api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(query, contexts, history):
    context_text = ""

    for i, ctx in enumerate(contexts):
        snippet = ctx["content"][:200]

        context_text += (
            f"[Source {i+1} | Page {ctx['page']} | ID {ctx['chunk_id']}]\n"
            f"{snippet}\n\n"
        )

    history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in history]
    )

    prompt = f"""
You are a strict document QA assistant.

Rules:
- Answer ONLY from context
- Cite sources like (Page X)
- If unsure, say "Not in document"
- Do NOT hallucinate
- Analyse the context, provide the answer with effectient and sufficient way.

Chat History:
{history_text}

Context:
{context_text}

Question:
{query}
"""

    return prompt

def generate_answer(query, contexts, history):
    # Build improved prompt (with history + citations)
    prompt = build_prompt(query, contexts, history)

    print("printing generation prompt", prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise document QA assistant. "
                        "Only answer from provided context."
                        "Always include citations (Page X)."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Error generating response: {str(e)}"

    return answer