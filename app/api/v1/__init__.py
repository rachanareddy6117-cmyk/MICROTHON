from fastapi import APIRouter
from .projects import router as projects_router
from .repositories import router as repositories_router
from .scans import router as scans_router
from .findings import router as findings_router
from .crypto_assets import router as crypto_assets_router
from .dependencies import router as dependencies_router
from .certificates import router as certificates_router
from .agents import router as agents_router
from .investigations import router as investigations_router
from .remediations import router as remediations_router
from .sandbox import router as sandbox_router
from .migrations import router as migrations_router
from .crypto_agility import router as crypto_agility_router
from .firewall import router as firewall_router
from .ci import router as ci_router
from .secure_data import router as secure_data_router
from .reports import router as reports_router
from .audit import router as audit_router
from .evaluation import router as evaluation_router
from .ws import router as ws_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(projects_router)
api_v1_router.include_router(repositories_router)
api_v1_router.include_router(scans_router)
api_v1_router.include_router(findings_router)
api_v1_router.include_router(crypto_assets_router)
api_v1_router.include_router(dependencies_router)
api_v1_router.include_router(certificates_router)
api_v1_router.include_router(agents_router)
api_v1_router.include_router(investigations_router)
api_v1_router.include_router(remediations_router)
api_v1_router.include_router(sandbox_router)
api_v1_router.include_router(migrations_router)
api_v1_router.include_router(crypto_agility_router)
api_v1_router.include_router(firewall_router)
api_v1_router.include_router(ci_router)
api_v1_router.include_router(secure_data_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(audit_router)
api_v1_router.include_router(evaluation_router)
api_v1_router.include_router(ws_router)
