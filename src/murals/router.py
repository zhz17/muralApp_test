from fastapi import APIRouter, Depends, HTTPException, Cookie
from typing import List, Annotated
from src.murals.schemas import SquareCreate
from src.murals.service import mural_service

router = APIRouter()

# --- 新的依赖项：从 Cookie 获取 Token ---
def get_token_from_cookie(mural_access_token: Annotated[str | None, Cookie()] = None):
    if not mural_access_token:
        raise HTTPException(status_code=401, detail="未授权，请先重新登录")
    return mural_access_token

# --- 1. 验证 Mural ID ---
@router.get("/{mural_id}/verify")
def verify_mural_id(
    mural_id: str, 
    token: str = Depends(get_token_from_cookie)
):
    try:
        info = mural_service.get_mural_details(mural_id, token)
        return {"id": info["id"], "title": info["title"]}
    except ValueError:
        raise HTTPException(status_code=404, detail="Mural ID 不存在")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- 2. 批量提交 (接收 JSON List) ---
@router.post("/{mural_id}/batch-shapes")
def batch_create_shapes(
    mural_id: str, 
    shapes: List[SquareCreate], # FastAPI 会自动验证 JSON 列表格式
    token: str = Depends(get_token_from_cookie)
):
    # 这里 shapes 已经被 Pydantic 验证并转换成了对象列表
    return mural_service.create_shapes_batch(mural_id, shapes, token)