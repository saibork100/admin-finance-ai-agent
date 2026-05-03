from langchain.tools import tool
from app.rag.retriever import query_documents


@tool
def search_documents(query: str) -> str:
    """
    Search uploaded documents (PDFs, contracts, invoices) using semantic search.
    Returns the most relevant excerpts with source references.
    Use this when the user asks about document contents.
    """
    results = query_documents(query)
    if not results:
        return "No relevant documents found for that query."
    return results


@tool
def draft_chase_email(invoice_id: str, client_name: str, amount: str, due_date: str) -> str:
    """
    Draft a professional email to chase a late invoice payment.
    Provide invoice_id, client_name, amount (e.g. '£1,200'), and due_date (e.g. '1 April 2025').
    """
    return f"""Subject: Payment Reminder — Invoice {invoice_id}

Dear {client_name},

I hope this message finds you well. I'm writing to follow up on Invoice {invoice_id}
for {amount}, which was due on {due_date}.

Could you please let me know when we can expect payment, or if there are any issues
I can help resolve? I'd appreciate your prompt attention to this matter.

Please don't hesitate to get in touch if you have any questions.

Kind regards,
[Your Name]"""


def get_document_tools():
    return [search_documents, draft_chase_email]
