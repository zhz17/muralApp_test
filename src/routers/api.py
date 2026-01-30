from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
from src.api.mural_client import MuralClient
import logging
import io

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate")
async def generate_mural(
    auth_token: str = Form(...),
    workspace_id: str = Form(...),
    json_text: Optional[str] = Form(None),
    json_file: Optional[UploadFile] = File(None)
):
    try:
        data = None
        if json_file:
            content = await json_file.read()
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON file")
        elif json_text:
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON text")
        else:
            raise HTTPException(status_code=400, detail="No JSON input provided")

        if not isinstance(data, list):
             raise HTTPException(status_code=400, detail="JSON must be a list of mural definitions")

        client = MuralClient(auth_token, workspace_id)
        results = client.process_json(data)
        
        return {"status": "success", "results": results}

    except Exception as e:
        logger.exception("Error during generation")
        raise HTTPException(status_code=500, detail=str(e))
