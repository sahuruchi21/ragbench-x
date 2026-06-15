import os
import re
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ============================
# GROQ GENERATION
# ============================
def generate_with_groq(
    query: str,
    context_chunks: List[str],
    model: str = "llama-3.3-70b-versatile"
) -> str:

    try:
        from groq import Groq

    except ImportError:
        raise RuntimeError(
            "groq not installed. Run: pip install groq"
        )

    try:

        api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not set"
            )

        client = Groq(
            api_key=api_key
        )

        context = "\n\n".join(
            context_chunks[:10]
        )[:6000]

        prompt = f"""You are an expert Retrieval-Augmented Generation (RAG) assistant.

Your task is to answer the question using ONLY the provided context below.

STRICT RULES:
1. Answer using ONLY information from the context — do not use external knowledge or introduce new facts.
2. Directness & Relevancy: Start your answer by repeating key terms and nouns from the question to state the response directly (e.g. if the question is "How does compound interest work?", start with "Compound interest works by...").
3. Faithfulness: Every content word in your answer must be supported by the context. Do not use external verbs, adjectives, or conversational fillers (such as "In addition", "Furthermore", "As stated in", "Based on the text") that are not present in the context.
4. Keep your answer concise, consisting of 2-4 sentences that cover the information available and remain close to verbatim from the context.
5. Do NOT add opinions, disclaimers, or information beyond the context.
6. Only if the context contains absolutely no information related to the question, respond with exactly:
   "The information is not available in the provided context."

Context:
{context}

Question:
{query}

Answer:"""

        completion = (
            client.chat.completions.create(

                model=model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.0,
                max_tokens=300
            )
        )

        return (
            completion
            .choices[0]
            .message.content
            .strip()
        )

    except Exception as e:

        raise RuntimeError(
            f"Groq error: {e}"
        )
# ============================
# TEMPLATE FALLBACK
# ============================
def generate_with_template(
    query: str,
    context_chunks: List[str]
) -> str:

    query_lower = query.lower()

    query_words = set(
        re.findall(r'\b[a-z]+\b', query_lower)
    )

    question_words = {
        'what', 'how', 'why', 'when', 'where', 'who',
        'which', 'does', 'is', 'are', 'do', 'can',
        'the', 'a', 'an'
    }

    query_keywords = query_words - question_words

    all_text = " ".join(context_chunks)

    sentences = re.split(
        r'(?<=[.!?])\s+',
        all_text
    )

    scored = []

    for s in sentences:

        words = set(
            re.findall(r'\b[a-z]+\b', s.lower())
        )

        overlap = len(query_keywords & words)

        if overlap > 0:
            scored.append((s.strip(), overlap))

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    if scored:
        return " ".join(
            [s[0] for s in scored[:4]]
        )

    elif context_chunks:
        return context_chunks[0][:500]

    else:
        return "No answer found in the provided context."


# ============================
# MAIN DISPATCH
# ============================
def generate_answer(
    query: str,
    context_chunks: List[str],
    provider: str = "groq",
    model_name: Optional[str] = None,
    is_custom: bool = False,
) -> str:

    if provider == "groq":

        return generate_with_groq(
            query,
            context_chunks,
            model=model_name or "llama-3.3-70b-versatile",
        )

    elif provider == "template":

        return generate_with_template(
            query,
            context_chunks,
        )

    else:
        raise ValueError(
            f"Unknown provider: {provider}. "
            f"Choose from: groq, template"
        )