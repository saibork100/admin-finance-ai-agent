from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.api.routes import agent, documents, finance, auth

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Admin & Finance AI Agent...")
    yield
    print("Shutting down...")


app = FastAPI(
    title="Admin & Finance AI Agent",
    description="Autonomous LLM agent for administrative and financial task management.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(finance.router, prefix="/finance", tags=["Finance"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "admin-finance-ai-agent"}
