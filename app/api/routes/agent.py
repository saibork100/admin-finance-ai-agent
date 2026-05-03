from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.auth import get_current_user
from app.agent.agent import get_agent

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    chat_history: list[dict] = []


class QueryResponse(BaseModel):
    answer: str
    tools_used: list[str] = []


@router.post("/query", response_model=QueryResponse)
async def query_agent(
    request: QueryRequest,
    current_user: str = Depends(get_current_user),
):
    try:
        agent_executor = get_agent()
        result = agent_executor.invoke({
            "input": request.query,
            "chat_history": request.chat_history,
        })

        # Extract which tools were used from intermediate steps
        tools_used = []
        for step in result.get("intermediate_steps", []):
            if step and hasattr(step[0], "tool"):
                tools_used.append(step[0].tool)

        return QueryResponse(
            answer=result.get("output", ""),
            tools_used=list(set(tools_used)),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
