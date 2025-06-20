from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json
from typing import Dict, Optional
from tag_manager import registered_tags
from datetime import datetime


# Simulated i18n message source (dictionary-based)
messages: Dict[str, Dict[str, str]] = {
    "en": {
        "tag_already_registered": "Tag ID already registered",
        "tag_not_found": "Tag not found",
        "tag_not_in_storage": "Tag ID not found in storage",
        "invalid_json": "Invalid JSON file",
        "file_not_found": "Storage file not found"
    }
}

def get_message(key: str, lang: str = "en") -> str:
    """Get localized message based on language code."""
    return messages.get(lang, messages["en"]).get(key, key)

# Pydantic model for POST /tags
class TagInput(BaseModel):
    id: str
    description: str

# Pydantic model for Tag response
class TagResponse(BaseModel):
    id: str
    description: str
    last_cnt: Optional[int]
    last_seen: Optional[str]

# FastAPI app
app = FastAPI()

def check_tag_in_storage(tag_id: str) -> bool:
    """Check if tag_id exists in tag_data_storage.json."""
    try:
        with open('./log/simulator_tag_data_storage.json', 'r') as file:
            data = json.load(file)
        if tag_id in data:
            return True, data[tag_id].get("cnt")
        return False, None
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=get_message("file_not_found"))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=get_message("invalid_json"))

@app.post("/tags", response_model=TagResponse)
async def register_tag(tag: TagInput, accept_language: str = "en"):
    """Register a new tag if it exists in tag_data_storage.json."""
    # Check if tag ID is already registered
    if tag.id in registered_tags:
        raise HTTPException(status_code=400, detail=get_message("tag_already_registered", accept_language))
    
    # Check if tag ID exists in tag_data_storage.json
    exists, cnt = check_tag_in_storage(tag.id)
    if not exists:
        raise HTTPException(status_code=400, detail=get_message("tag_not_in_storage", accept_language))
    
    # Register the tag
    registered_tags[tag.id] = {
        "id": tag.id,
        "description": tag.description,
        "last_cnt": cnt,
        "last_seen": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    }
    return registered_tags[tag.id]

@app.get("/tags", response_model=list[TagResponse])
async def get_tags():
    """Get list of registered tags with their status."""
    return list(registered_tags.values())

@app.get("/tag/{id}", response_model=TagResponse)
async def get_tag(id: str, accept_language: str = "en"):
    """Get status of a single tag by ID."""
    if id not in registered_tags:
        raise HTTPException(status_code=404, detail=get_message("tag_not_found", accept_language))
    return registered_tags[id]

@app.get("/health")
async def health_check():
    """Check system health."""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)