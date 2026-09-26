from __future__ import annotations

import re
from pathlib import Path
from typing import List

import faiss
import pymupdf
import numpy as np
from sentence_transformers import SentenceTransformer


DEFAULT_SOURCE_TEXT = """
Post-quantum cryptography guidance.

1. Weak key generation is a cryptographic flaw when the entropy source is insufficient or predictable.
2. The fix is to use a cryptographically secure random number generator and validate entropy quality before key creation.
3. Side-channel leakage can expose private keys during implementation, especially in embedded or shared-memory systems.
4. The fix is to harden implementations, use constant-time logic, and test against power and timing analysis.
5. Unverified parameter choices create risk in lattice or code-based systems.
6. The fix is to use standards-approved parameter sets and peer-reviewed implementations.
7. Poor key management creates long-term exposure when keys are stored insecurely or reused across contexts.
8. The fix is to rotate keys, separate storage domains, and enforce secure expiry and revocation policies.
9. Weak certificate validation leads to MITM or downgrade attacks.
10. The fix is to enforce strict certificate chain checks, validated algorithms, and secure TLS configuration.
11. Incomplete memory zeroization can leave secrets recoverable after use.
12. The fix is to erase sensitive buffers after use and follow secure cleanup requirements.
13. Using outdated or non-standard crypto primitives is a serious design flaw.
14. The fix is to prefer NIST-approved post-quantum algorithms and avoid deprecated schemes.
15. Insecure implementation of KEM or signature wrappers can break the protection expected from the primitive itself.
16. The fix is to validate API boundaries and use well-tested reference code.
17. Reusing ephemeral keys or non-random nonces can create predictable cryptographic output.
18. The fix is to generate fresh random values for each operation and verify protocol compliance.
"""


def find_pdf_path() -> str | None:
    candidates = [
        Path(r"C:\Users\Rachana Reddy\Downloads\crypto_flaws_and_fixes.pdf"),
        Path(r"C:\Users\Rachana Reddy\OneDrive\Desktop\crypto_flaws_and_fixes.pdf"),
        Path(r"C:\Users\Rachana Reddy\OneDrive\Desktop\Post quantum cryptogarphy model\crypto_flaws_and_fixes.pdf"),
    ]
    for target in candidates:
        if target.exists():
            return str(target)
    return None


def clean_text(raw_text: str) -> str:
    if not raw_text:
        return ""

    text = raw_text.replace("\r", "\n")
    lines = []
    for line in text.split("\n"):
        cleaned = re.sub(r"\s+", " ", line).strip()
        cleaned = cleaned.replace("\u00a0", " ")
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if len(cleaned) < 8:
            continue
        if any(token in lowered for token in ["page ", "figure ", "table ", "copyright", "all rights reserved", "lorem ipsum", "random junk", "placeholder", "www."]):
            continue
        if re.fullmatch(r"[-_=#*]+", cleaned):
            continue
        if lowered.startswith("http"):
            continue
        lines.append(cleaned)

    return "\n".join(lines)


def extract_pdf_text(pdf_path: str | None = None) -> str:
    pdf_target = pdf_path or find_pdf_path()
    if pdf_target:
        with pymupdf.open(pdf_target) as document:
            pages = [page.get_text("text") for page in document]
        raw_text = "\n".join(pages)
        return clean_text(raw_text)
    return clean_text(DEFAULT_SOURCE_TEXT)


def chunk_text(text: str, chunk_size: int = 250, overlap: int = 40) -> List[str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    chunks: List[str] = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) <= chunk_size:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(current)
            current = sentence
        if len(current) >= chunk_size:
            chunks.append(current)
            current = current[-overlap:] if overlap else ""

    if current:
        chunks.append(current)

    return [chunk for chunk in chunks if chunk]


class LocalCryptoLLM:
    def __init__(self, pdf_path: str | None = None, model_name: str = "all-MiniLM-L6-v2"):
        self.pdf_path = pdf_path or find_pdf_path()
        source_text = extract_pdf_text(self.pdf_path)
        self.chunks = chunk_text(source_text)
        if not self.chunks:
            raise ValueError("No valid text was generated from the PDF or fallback data.")

        self.model = SentenceTransformer(model_name)
        embeddings = self.model.encode(self.chunks, convert_to_numpy=True, normalize_embeddings=True)
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(np.asarray(embeddings, dtype=np.float32))

    def ask(self, question: str, top_k: int = 3) -> str:
        if not question or not question.strip():
            raise ValueError("A question is required.")

        query_vector = self.model.encode([question.strip()], convert_to_numpy=True, normalize_embeddings=True)
        _, indices = self.index.search(np.asarray(query_vector, dtype=np.float32), top_k)

        context = "\n".join(self.chunks[int(i)] for i in indices[0] if int(i) < len(self.chunks))
        if not context:
            return "No relevant cryptography guidance was found in the cleaned dataset."

        answer = (
            "Retrieved reference text relevant to your question:\n\n"
            f"{context}\n\n"
            "General reminder: validate cryptographic choices against current standards, reviewed implementations, and your organization's security policy."
        )
        return answer


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Local cryptography PDF retrieval demo (not a trained generative LLM).")
    parser.add_argument("--pdf", type=str, default=None, help="Path to the crypto PDF file.")
    parser.add_argument("--question", type=str, default="How can weak key generation and poor key management be fixed?", help="Question to answer.")
    args = parser.parse_args()

    llm = LocalCryptoLLM(pdf_path=args.pdf)
    print(llm.ask(args.question))
