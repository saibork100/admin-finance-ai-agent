from pathlib import Path
from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.auth import get_current_user
from app.agent.tools.finance_tools import summarise_expenses, list_outstanding_invoices

router = APIRouter()

UPLOAD_DIR = Path("./data/uploads").resolve()


def _safe_upload_path(filename: str) -> str:
    """Resolve filename to upload dir, rejecting any path traversal."""
    resolved = (UPLOAD_DIR / Path(filename).name).resolve()
    if not str(resolved).startswith(str(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="Invalid filename.")
    return str(resolved)


@router.get("/summary")
async def finance_summary(
    filename: str = Query(..., description="Filename of expenses CSV in uploads dir"),
    month: str = Query(None, description="Filter by month e.g. 2025-03"),
    current_user: str = Depends(get_current_user),
):
    result = summarise_expenses.invoke({"filepath": _safe_upload_path(filename), "month": month})
    return {"summary": result}


@router.get("/invoices/outstanding")
async def outstanding_invoices(
    filename: str = Query(..., description="Filename of invoices CSV in uploads dir"),
    current_user: str = Depends(get_current_user),
):
    result = list_outstanding_invoices.invoke({"filepath": _safe_upload_path(filename)})
    return {"invoices": result}
