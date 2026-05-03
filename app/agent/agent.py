import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from app.agent.tools.finance_tools import get_finance_tools
from app.agent.tools.document_tools import get_document_tools

SYSTEM_PROMPT = """You are an intelligent admin and finance assistant for a small business.
You have access to tools that can:
- Search and retrieve information from uploaded documents (invoices, contracts, reports)
- Analyse financial data from CSV files
- Draft professional emails and summaries

Always be concise, professional, and accurate. When referencing documents, cite the source.
If you cannot find the information requested, say so clearly."""


def build_agent() -> AgentExecutor:
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        streaming=False,
    )

    tools = get_finance_tools() + get_document_tools()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )


# Singleton — initialised once on first call
_agent_executor: AgentExecutor | None = None


def get_agent() -> AgentExecutor:
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = build_agent()
    return _agent_executor
