"""
RAGBench-X Embedding Module
Supports: TF-IDF (baseline), BGE-large, E5-mistral
"""

import math
import re
from typing import List, Dict
from collections import Counter


# ============================
# TF-IDF EMBEDDER (Baseline)
# ============================

class TFIDFEmbedder:
    """
    Simple TF-IDF vectorizer — no external dependencies needed.
    Perfect for benchmarking without GPU requirements.
    """
    
    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.fitted = False
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple word tokenization."""
        text = text.lower()
        tokens = re.findall(r'\b[a-z]+\b', text)
        # Remove common stop words
        stop_words = {
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
            'also', 'about', 'up', 'out', 'down',
        }
        return [t for t in tokens if t not in stop_words and len(t) > 1]
    
    def fit(self, documents: List[str]):
        """Build vocabulary and IDF weights from documents."""
        doc_count = len(documents)
        doc_freq: Dict[str, int] = Counter()
        
        for doc in documents:
            tokens = set(self._tokenize(doc))
            for token in tokens:
                doc_freq[token] += 1
        
        # Build vocabulary
        self.vocabulary = {word: idx for idx, word in enumerate(doc_freq.keys())}
        
        # Compute IDF
        self.idf = {
            word: math.log((doc_count + 1) / (freq + 1)) + 1
            for word, freq in doc_freq.items()
        }
        self.fitted = True
    
    def embed(self, text: str) -> List[float]:
        """Convert text to TF-IDF vector."""
        if not self.fitted:
            raise RuntimeError("Embedder not fitted. Call fit() first.")
        
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        
        vector = [0.0] * len(self.vocabulary)
        for word, count in tf.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                vector[idx] = (count / total) * self.idf.get(word, 1.0)
        
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        return [self.embed(text) for text in texts]


# ============================
# TRANSFORMER EMBEDDER (BGE, E5)
# ============================

class TransformerEmbedder:
    """
    Transformer-based embeddings using sentence-transformers.
    Supports BGE, E5, and other Hugging Face models.
    """
    
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading {model_name}... (first time will download ~500MB)")
            self.model = SentenceTransformer(model_name)
            self.fitted = True
            print(f"✓ {model_name} loaded successfully")
        except ImportError:
            raise RuntimeError(
                "sentence-transformers not installed. "
                "Run: pip install sentence-transformers"
            )
    
    def fit(self, documents: List[str]):
        """Pre-trained models don't need fitting."""
        pass
    
    def embed(self, text: str) -> List[float]:
        """Convert text to dense vector."""
        return self.model.encode(text, convert_to_numpy=True).tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts efficiently."""
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False).tolist()


# ============================
# UTILITY FUNCTIONS
# ============================

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a)) or 1.0
    norm_b = math.sqrt(sum(b * b for b in vec_b)) or 1.0
    return dot / (norm_a * norm_b)


# ============================
# FACTORY FUNCTION
# ============================

def get_embedding_model(model_type: str = "bge"):
    """
    Factory function to create an embedding model.
    
    Args:
        model_type: "tfidf", "bge", or "e5"
    
    Returns:
        Embedder instance
    """
    if model_type == "tfidf":
        return TFIDFEmbedder()
    elif model_type == "bge":
        return TransformerEmbedder("BAAI/bge-base-en-v1.5")
    elif model_type == "e5":
        return TransformerEmbedder("intfloat/e5-base-v2")
    else:
        raise ValueError(
            f"Unknown embedding model: {model_type}. "
            f"Choose from: tfidf, bge, e5"
        )