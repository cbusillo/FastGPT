from fastapi import APIRouter
from components.lang_model_service import LLMClient

router = APIRouter()


@router.get("/models")
async def get_models() -> dict[str, list[str]]:
    return {"models": LLMClient.get_model_names()}
