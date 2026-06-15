"""
RAGBench-X Chunking Strategies
Supports multiple chunking approaches for benchmarking comparison.
"""

from typing import List, Dict


def chunk_fixed_size(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Fixed-size character chunking with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]


def chunk_sentence(text: str, sentences_per_chunk: int = 3) -> List[str]:
    """Sentence-based chunking."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks


def chunk_paragraph(text: str) -> List[str]:
    """Paragraph-based chunking — splits on double newlines."""
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]


def chunk_semantic(text: str, max_chunk_size: int = 300) -> List[str]:
    """
    Semantic chunking — tries to split on topic boundaries.
    Uses sentence splitting + merging based on size limits.
    Carries the last sentence of each chunk into the next (overlap)
    to prevent relevant context from being split at boundaries.
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    last_sentence = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk = (current_chunk + " " + sentence).strip()
            last_sentence = sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # Carry last sentence as overlap into new chunk
            if last_sentence and last_sentence != sentence:
                current_chunk = (last_sentence + " " + sentence).strip()
            else:
                current_chunk = sentence
            last_sentence = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


CHUNKING_STRATEGIES = {
    "fixed": chunk_fixed_size,
    "sentence": chunk_sentence,
    "paragraph": chunk_paragraph,
    "semantic": chunk_semantic,
}


def chunk_documents(documents: List[str], strategy: str = "semantic", **kwargs) -> List[str]:
    """
    Chunk a list of document texts using the specified strategy.
    Returns flat list of chunk strings.
    """
    if strategy not in CHUNKING_STRATEGIES:
        raise ValueError(f"Unknown strategy: {strategy}. Choose from: {list(CHUNKING_STRATEGIES.keys())}")
    
    chunker = CHUNKING_STRATEGIES[strategy]
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunker(doc, **kwargs))
    return all_chunks