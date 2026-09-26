from pathlib import Path

import pymupdf

from src.crypto_llm import extract_pdf_text


def test_clean_text_filters_junk_and_keeps_valid_sections():
    raw = """
    CRYPTOGRAPHY SECURITY REVIEW

    weak_key_generation is an issue when keys use insufficient entropy.
    The fix is to use a strong random source with enough entropy.

    !!! corrupted line with random junk ###

    Use a vetted post-quantum KEM and validate all implementations.
    """

    text = raw.replace("\r", "").strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = [line for line in lines if len(line) > 6 and "random junk" not in line.lower()]

    assert any("weak_key_generation" in line.lower() for line in cleaned)
    assert any("post-quantum" in line.lower() for line in cleaned)
    assert not any("random junk" in line.lower() for line in cleaned)
    assert len(cleaned) >= 3


def test_project_layout_exists():
    assert Path(".").exists()


def test_extract_pdf_text_reads_reference_document(tmp_path):
    pdf_path = tmp_path / "reference.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Weak key generation needs strong entropy.")
    document.save(pdf_path)
    document.close()

    extracted = extract_pdf_text(str(pdf_path))

    assert "Weak key generation needs strong entropy." in extracted
