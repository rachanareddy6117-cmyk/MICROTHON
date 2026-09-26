from pathlib import Path

import pymupdf


OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "PQC-Migrate-Tech-Stack.pdf"


def main() -> None:
    document = pymupdf.open()
    page = document.new_page(width=595, height=842)

    page.draw_rect(pymupdf.Rect(0, 0, 595, 98), color=(0.035, 0.075, 0.13), fill=(0.035, 0.075, 0.13))
    page.insert_text((48, 44), "PQC-Migrate", fontsize=24, fontname="hebo", color=(1, 1, 1))
    page.insert_text((48, 73), "TECH STACK · QUICK SUMMARY", fontsize=10, fontname="hebo", color=(0.25, 0.83, 0.76))

    items = [
        ("Frontend", "HTML, CSS, JavaScript"),
        ("Backend", "Python 3.12 · FastAPI · Uvicorn"),
        ("Data", "PostgreSQL · SQLAlchemy · Alembic · SQLite demo data"),
        ("Cache / queue", "Redis (container included; worker dispatch not wired)"),
        ("PDF / retrieval", "PyMuPDF · Sentence Transformers · FAISS · NumPy"),
        ("Security libraries", "cryptography · pyOpenSSL · PyJWT"),
        ("Containers", "Docker · Docker Compose"),
        ("Testing", "pytest · Node.js syntax check"),
        ("Tools", "VS Code · Git · GitHub"),
    ]

    y = 143
    for label, value in items:
        page.insert_text((50, y), label, fontsize=11, fontname="hebo", color=(0.035, 0.075, 0.13))
        page.insert_text((190, y), value, fontsize=10, fontname="helv", color=(0.16, 0.23, 0.29))
        page.draw_line((50, y + 12), (545, y + 12), color=(0.86, 0.89, 0.91), width=0.5)
        y += 39

    page.draw_rect(pymupdf.Rect(48, 515, 547, 637), color=(0.91, 0.96, 0.95), fill=(0.91, 0.96, 0.95))
    page.insert_text((64, 543), "Model status", fontsize=12, fontname="hebo", color=(0.035, 0.075, 0.13))
    page.insert_textbox(
        pymupdf.Rect(64, 555, 528, 620),
        "Local PDF retrieval demo only: pretrained all-MiniLM-L6-v2 embeddings + FAISS search. It is not a trained or generative LLM.",
        fontsize=10,
        fontname="helv",
        color=(0.16, 0.23, 0.29),
        lineheight=1.35,
    )

    page.insert_textbox(
        pymupdf.Rect(50, 663, 540, 735),
        "Prototype note: PostgreSQL, Redis, and Docker are included, but scan/policy persistence, background jobs, production login/RBAC, KMS/HSM, and live firewall enforcement are not connected.",
        fontsize=9.5,
        fontname="helv",
        color=(0.36, 0.43, 0.48),
        lineheight=1.4,
    )
    page.draw_line((50, 790), (545, 790), color=(0.82, 0.87, 0.90), width=0.6)
    page.insert_text((50, 811), "PQC-Migrate · concise technology overview", fontsize=8, fontname="helv", color=(0.42, 0.51, 0.58))

    document.set_metadata(
        {
            "title": "PQC-Migrate Tech Stack",
            "author": "PQC-Migrate",
            "subject": "Concise project tools and software overview",
        }
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUTPUT, garbage=4, deflate=True)
    document.close()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
