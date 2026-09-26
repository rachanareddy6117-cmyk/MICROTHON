from fastapi import APIRouter
from ...core.agility import agility_registry

router = APIRouter(prefix="/crypto-agility", tags=["Crypto Agility Layer"])

@router.get("/registry")
def get_agility_registry():
    return agility_registry.get_recommended_algorithms()
