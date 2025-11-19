import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Team, Application, Order

app = FastAPI(title="Nizard Gaming API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "Nizard Gaming API", "status": "ok"}

# Utility: convert ObjectId to string safely when returning documents

def serialize_doc(doc: dict):
    if not isinstance(doc, dict):
        return doc
    d = dict(doc)
    _id = d.get("_id")
    try:
        from bson import ObjectId
        if isinstance(_id, ObjectId):
            d["_id"] = str(_id)
    except Exception:
        if _id is not None:
            d["_id"] = str(_id)
    return d

# Public endpoints

@app.get("/api/products")
def list_products(limit: int = 50):
    try:
        docs = get_documents("product", {}, limit)
        return [serialize_doc(x) for x in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/apply")
def create_application(payload: Application):
    try:
        app_id = create_document("application", payload)
        return {"id": app_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/teams")
def list_teams(game: Optional[str] = None, limit: int = 50):
    try:
        q = {"game": game} if game else {}
        docs = get_documents("team", q, limit)
        return [serialize_doc(x) for x in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orders")
def create_order(payload: Order):
    try:
        order_id = create_document("order", payload)
        return {"id": order_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', "✅ Connected")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
