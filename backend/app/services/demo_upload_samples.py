from __future__ import annotations

from io import BytesIO
import zipfile

import pymupdf


def project_specification_pdf() -> bytes:
    document = pymupdf.open()
    page = document.new_page(width=595, height=842)
    page.insert_text((54, 58), "PQC-Migrate Demonstration Project", fontsize=19, fontname="hebo")
    content = (
        "Scope: Example payment API post-quantum migration assessment\n"
        "Technology: Python, Java, TLS 1.2, RSA, SHA-1\n"
        "Timeline: 12 weeks\n"
        "Budget: USD 25,000 planning allowance (demo input, not a quote)\n"
        "Vendors: Example Cloud, OpenSSL\n"
        "Dependencies: cryptography, requests, PostgreSQL\n"
        "Security requirements: TLS 1.3, certificate rotation, ML-KEM readiness\n"
        "Risks: Legacy RSA certificates, SHA-1 signature references, TLS 1.0 compatibility\n\n"
        "This is synthetic training/demo content. It contains no real credentials, keys, or customer data.\n"
        "The listed cryptographic references are deliberately included to demonstrate candidate evidence detection."
    )
    page.insert_textbox(
        pymupdf.Rect(54, 95, 540, 450),
        content,
        fontsize=11,
        fontname="helv",
        lineheight=1.5,
    )
    result = document.tobytes(garbage=4, deflate=True)
    document.close()
    return result


def software_bundle_zip() -> bytes:
    bundle = BytesIO()
    with zipfile.ZipFile(bundle, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "README.md",
            "# Synthetic software scanner sample\n"
            "This sample is for static analysis only. It is not built or executed.\n"
            "It contains no real secrets or private keys.\n",
        )
        archive.writestr(
            "requirements.txt",
            "cryptography==42.0.0\n"
            "requests>=2.0\n",
        )
        archive.writestr(
            "package.json",
            '{"name":"pqc-migrate-demo-sample","version":"1.0.0",'
            '"dependencies":{"example-package":"1.0.0"},'
            '"devDependencies":{"example-test-tool":"1.0.0"}}',
        )
        archive.writestr(
            "src/crypto_sample.py",
            "from hashlib import sha1\n"
            "digest = sha1(b'demo')\n"
            'signature_algorithm = "RSA-2048 with SHA-1"\n'
            'legacy_cipher = "3DES-CBC"\n'
            'private_key = "DEMO_ONLY_NOT_A_REAL_SECRET"\n'
            'note = "TLS 1.0 is a demo finding; this code is never executed"\n'
            'raise RuntimeError("scanner must not execute this sample")\n',
        )
        archive.writestr(
            "config/tls.yaml",
            "minimum_tls: TLS 1.0\n"
            "cipher: RC4-SHA\n"
            "pqc_target: ML-KEM\n",
        )
    return bundle.getvalue()
