from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()  # loads variables from .env

api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(query, contexts, history):
    context_text = ""

    for i, ctx in enumerate(contexts):
        snippet = ctx["content"]

        context_text += (
            f"[Source {i+1} | Page {ctx['page']} | ID {ctx['chunk_id']}]\n"
            f"{snippet}\n\n"
        )

    history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in history]
    )

    prompt = f"""
You are a helpful and precise document QA assistant.

Guidelines:
- Primarily use the provided context to answer.
- If the exact answer is not explicitly stated, you may make a reasonable inference based on the context.
- Prefer giving a useful, human-like answer rather than rejecting the question.
- If you infer, clearly indicate it (e.g., "Based on the context..." or "It can be inferred that...").
- If the question is completely unrelated to the context, politely say so.
- If you find the question refers to multiple context, try to consolidate and summarize things in detail and clear.4
- Never miss out any of the information found in context

Citation Rules:
- Cite sources like (Page X) when directly using context.
- If partially inferred, still ground your answer in the closest relevant context.

Key Note:
Context provided are retrieved from vector DB to provide information, summarize your answer accordingly.

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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Generative model used to summarize and provide answers in RAG application"
                        "You are a precise document QA assistant."
                        "Only answer from provided context."
                        "Always include citations (Page X)."
                        "Try to provide answers before completely saying not in the context"
                        "Also recommend a follow up questions each time in the end of answer from the retrieved context and history - 'can I type of question'"
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