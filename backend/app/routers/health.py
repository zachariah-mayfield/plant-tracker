from fastapi import APIRouter
from sqlalchemy import text
from ..database import engine

router = APIRouter()

@router.get("/db-check")
def db_check():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"db_alive": result.scalar() == 1}
    except Exception as e:
        return {"error": str(e)}

