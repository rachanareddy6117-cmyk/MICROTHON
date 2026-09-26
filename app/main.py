import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .config import settings
from .api.v1 import api_v1_router
from .database import init_db
from .core.disclaimer import LIMITATIONS_DISCLOSURE

app = FastAPI(
    title="PQC-Migrate API",
    description="Post-Quantum Cryptography Migration, Static Analysis, Defensive Firewall & Agile Remediation Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
def health():
    return {
        "status": "HEALTHY",
        "application": "PQC-Migrate",
        "version": "1.0.0",
        "philosophy": "Static Analysis + Defensive Policy Enforcement + Risk Communication (NOT Live Proof)"
    }

@app.get("/", response_class=HTMLResponse)
def index():
    return f"""<!DOCTYPE html>
<html>
<head>
  <title>PQC-Migrate API</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b0f19; color: #f1f5f9; padding: 2rem; }}
    .card {{ background: #151d30; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; max-width: 800px; margin: 0 auto; }}
    h1 {{ color: #00f2fe; margin-bottom: 0.5rem; }}
    .badge {{ background: rgba(255,170,0,0.2); color: #ffbb22; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }}
    a {{ color: #4facfe; text-decoration: none; font-weight: bold; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>PQC-Migrate Engine</h1>
    <p style="color: #94a3b8; margin-bottom: 1rem;">Post-Quantum Cryptography Static Analysis, Dependency Blast Radius & Migration Planning</p>
    <div style="background: rgba(255,170,0,0.1); border: 1px solid rgba(255,170,0,0.3); padding: 12px; border-radius: 8px; margin-bottom: 1rem;">
      <span class="badge">EPISTEMIC DISCLAIMER</span>
      <p style="font-size: 0.85rem; margin-top: 6px; color: #cbd5e1;">{LIMITATIONS_DISCLOSURE["warning_banner"]}</p>
    </div>
    <p>API Documentation: <a href="/docs">Interactive OpenAPI Swagger UI (/docs)</a></p>
    <p>Alternative Docs: <a href="/redoc">ReDoc (/redoc)</a></p>
  </div>
</body>
</html>"""
