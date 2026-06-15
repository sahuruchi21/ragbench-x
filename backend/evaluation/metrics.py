"""
RAGBench-X Evaluation Metrics
Scores RAG pipeline outputs on faithfulness, hallucination rate,
recall, answer relevancy and BLEU score.
"""

import re
import math
from typing import List, Dict, Optional
from collections import Counter


# ---------------------------------------------------
# Tokenisation helpers
# ---------------------------------------------------

STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'shall', 'can',
    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
    'as', 'into', 'through', 'during', 'before', 'after', 'and',
    'but', 'or', 'nor', 'not', 'so', 'yet', 'both', 'either',
    'neither', 'each', 'every', 'all', 'any', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'only', 'own',
    'same', 'than', 'too', 'very', 'just', 'because', 'it',
    'its', 'this', 'that', 'these', 'those', 'i', 'me', 'my',
    'we', 'our', 'you', 'your', 'he', 'him', 'his', 'she',
    'her', 'they', 'them', 'their', 'what', 'which', 'who',
    'whom', 'when', 'where', 'why', 'how', 'if', 'then',
    'also', 'about', 'up', 'out', 'down', 'there', 'here',
    'between', 'over', 'under', 'again', 'further', 'once',
}


def _simple_stem(word: str) -> str:
    """Lightweight suffix stemmer for better token matching.
    Strips common English suffixes so word variants match
    (e.g. 'remodelling' -> 'remodel', 'mitochondrial' -> 'mitochondri').
    """
    if len(word) <= 4:
        return word
    # Order matters: try longest suffixes first
    for suffix in (
        'ational', 'tional', 'encies', 'ances', 'ments',
        'ation', 'ness', 'ment', 'ence', 'ance', 'ible',
        'able', 'ting', 'sing', 'ling', 'ally', 'ious',
        'ical', 'ized', 'ises', 'ates', 'ated',
        'ing', 'ion', 'ity', 'ous', 'ive', 'ful',
        'ies', 'ial', 'ent', 'ant', 'ist', 'ism',
        'ers', 'als', 'ely', 'ory',
        'ly', 'ed', 'al', 'er', 'es',
    ):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    if word.endswith('s') and not word.endswith('ss') and len(word) > 4:
        return word[:-1]
    return word


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b[a-z]+\b", text.lower())


def _stemmed_tokens(text: str) -> List[str]:
    """Return stemmed tokens with stop words removed."""
    return [_simple_stem(t) for t in _tokenize(text) if t not in STOP_WORDS and len(t) > 1]


def _content_tokens(text: str) -> List[str]:
    """Return tokens with stop words removed."""
    return [t for t in _tokenize(text) if t not in STOP_WORDS and len(t) > 1]


def _get_ngrams(tokens: List[str], n: int):
    return [
        tuple(tokens[i:i+n])
        for i in range(len(tokens)-n+1)
    ]


# ---------------------------------------------------
# Faithfulness  (improved: uni + bi + trigram + boost)
# ---------------------------------------------------

def compute_faithfulness(
    answer: str,
    context_chunks: List[str]
) -> float:

    if not answer or not context_chunks:
        return 0.0

    context_text = " ".join(context_chunks).lower()
    context_tokens = _tokenize(context_text)

    context_unigrams = set(context_tokens)
    context_bigrams = set(_get_ngrams(context_tokens, 2))
    context_trigrams = set(_get_ngrams(context_tokens, 3))

    answer_tokens = _tokenize(answer)

    if not answer_tokens:
        return 0.0

    # Also build stemmed sets for fallback matching
    context_stemmed = set(_simple_stem(t) for t in context_tokens)

    content_tokens = [
        t for t in answer_tokens
        if t not in STOP_WORDS and len(t) > 1
    ]

    if not content_tokens:
        return 0.5

    # --- Unigram score (with stemmed fallback) ---
    unigram_hits = 0
    for t in content_tokens:
        if t in context_unigrams:
            unigram_hits += 1
        elif _simple_stem(t) in context_stemmed:
            unigram_hits += 0.85  # partial credit for stem match
    uni_score = unigram_hits / len(content_tokens)

    # --- Bigram score ---
    answer_bigrams = _get_ngrams(answer_tokens, 2)
    if answer_bigrams:
        bigram_hits = sum(
            1 for bg in answer_bigrams
            if bg in context_bigrams
        )
        bi_score = bigram_hits / len(answer_bigrams)
    else:
        bi_score = uni_score

    # --- Trigram score ---
    answer_trigrams = _get_ngrams(answer_tokens, 3)
    if answer_trigrams:
        trigram_hits = sum(
            1 for tg in answer_trigrams
            if tg in context_trigrams
        )
        tri_score = trigram_hits / len(answer_trigrams)
    else:
        tri_score = bi_score

    # Weighted combination: uni 45%, bi 35%, tri 20%
    raw_score = 0.45 * uni_score + 0.35 * bi_score + 0.20 * tri_score

    # Semantic boost: if most content words appear in context, reward
    if uni_score >= 0.6:
        raw_score = min(raw_score * 1.15, 1.0)

    return round(min(raw_score, 1.0), 4)


# ---------------------------------------------------
# Hallucination (inverse of faithfulness)
# ---------------------------------------------------

def compute_hallucination_rate(
    answer: str,
    context_chunks: List[str]
):

    faithfulness = compute_faithfulness(
        answer,
        context_chunks
    )

    return round(1 - faithfulness, 4)


# ---------------------------------------------------
# Recall@K  (improved: stemmed content-token recall)
# ---------------------------------------------------

def compute_recall_at_k(
    gold_answer: str,
    retrieved_chunks: List[str]
):

    if not gold_answer:
        return None

    if not retrieved_chunks:
        return 0.0

    retrieved_text = " ".join(retrieved_chunks)

    # Primary: stemmed content tokens (handles word variants)
    gold_stemmed = set(_stemmed_tokens(gold_answer))
    retrieved_stemmed = set(_stemmed_tokens(retrieved_text))

    # Fallback: raw content tokens
    gold_raw = set(_content_tokens(gold_answer))
    retrieved_raw = set(_content_tokens(retrieved_text))

    # Final fallback: all tokens
    if not gold_stemmed and not gold_raw:
        gold_raw = set(_tokenize(gold_answer))
        retrieved_raw = set(_tokenize(retrieved_text))

    if not gold_stemmed and not gold_raw:
        return None

    # Stemmed recall (more forgiving — word variants match)
    if gold_stemmed:
        stemmed_overlap = len(gold_stemmed & retrieved_stemmed)
        stemmed_recall = stemmed_overlap / len(gold_stemmed)
    else:
        stemmed_recall = 0.0

    # Raw recall (exact match)
    if gold_raw:
        raw_overlap = len(gold_raw & retrieved_raw)
        raw_recall = raw_overlap / len(gold_raw)
    else:
        raw_recall = 0.0

    # Take the better of the two (stemmed usually wins)
    recall = max(stemmed_recall, raw_recall)

    return round(recall, 4)


# ---------------------------------------------------
# Answer Relevancy  (improved: Jaccard + coverage bonus)
# ---------------------------------------------------

def compute_answer_relevancy(
    question: str,
    answer: str
):

    if not question or not answer:
        return 0.0

    q_content = set(_stemmed_tokens(question))
    a_content = set(_stemmed_tokens(answer))

    # Fall back to raw tokens if content filtering empties everything
    if not q_content:
        q_content = set([_simple_stem(t) for t in _tokenize(question)])
    if not a_content:
        a_content = set([_simple_stem(t) for t in _tokenize(answer)])

    if not q_content or not a_content:
        return 0.5

    # Jaccard-style: overlap / smaller set
    overlap = len(q_content & a_content)
    score = overlap / min(len(q_content), len(a_content))

    # Keyword coverage bonus: if answer covers ≥80% of question keywords
    coverage = overlap / len(q_content)
    if coverage >= 0.8:
        score = min(score * 1.10, 1.0)

    # Length penalty: if answer is extremely short (< 5 content tokens)
    # and question has many, penalise slightly
    if len(a_content) < 5 and len(q_content) > 5:
        score *= 0.9

    return round(min(score, 1.0), 4)


# ---------------------------------------------------
# BLEU  (kept for display, excluded from overall)
# ---------------------------------------------------

def compute_bleu_score(
    generated: str,
    reference: str
):

    if not generated or not reference:
        return None

    gen = _tokenize(generated)
    ref = _tokenize(reference)

    if not gen or not ref:
        return None

    precisions = []

    for n in range(1, 5):

        gen_ng = Counter(_get_ngrams(gen, n))
        ref_ng = Counter(_get_ngrams(ref, n))

        total = sum(gen_ng.values())

        if total == 0:
            precisions.append(0)
            continue

        matches = sum(
            min(count, ref_ng.get(g, 0))
            for g, count in gen_ng.items()
        )

        precisions.append(matches / total)

    smoothed = [max(p, 1e-10) for p in precisions]

    bleu = math.exp(
        sum(math.log(p) for p in smoothed) / 4
    )

    return round(bleu, 4)


# ---------------------------------------------------
# Final evaluation  (BLEU excluded from overall)
# ---------------------------------------------------

def evaluate_answer(
    question: str,
    generated_answer: str,
    gold_answer: str,
    context_chunks: List[str],
    retrieved_chunks: List[str]
) -> Dict:

    faithfulness = compute_faithfulness(
        generated_answer,
        context_chunks
    )

    hallucination = compute_hallucination_rate(
        generated_answer,
        context_chunks
    )

    recall = compute_recall_at_k(
        gold_answer,
        retrieved_chunks
    )

    relevancy = compute_answer_relevancy(
        question,
        generated_answer
    )

    bleu = compute_bleu_score(
        generated_answer,
        gold_answer
    )

    # --- Weighted overall (BLEU excluded, no double-counting) ---
    # Note: hallucination = 1 - faithfulness, so we use only faithfulness
    # to avoid double-counting the same metric.
    if recall is not None:
        # Weights: faithfulness 40%, recall 35%, relevancy 25%
        overall = round(
            0.40 * faithfulness +
            0.35 * recall +
            0.25 * relevancy,
            4
        )
    else:
        # No gold answer: faithfulness 55%, relevancy 45%
        overall = round(
            0.55 * faithfulness +
            0.45 * relevancy,
            4
        )

    return {
        "faithfulness": faithfulness,
        "hallucination_rate": hallucination,
        "recall_at_k": recall,
        "answer_relevancy": relevancy,
        "bleu_score": bleu,
        "overall_score": overall
    }