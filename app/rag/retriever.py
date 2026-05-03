from app.rag.indexer import get_index


def query_documents(query: str, top_k: int = 4) -> str:
    """
    Query the vector store and return relevant document excerpts.
    """
    try:
        index = get_index()
        query_engine = index.as_query_engine(similarity_top_k=top_k)
        response = query_engine.query(query)

        if not str(response).strip():
            return "No relevant content found."

        sources = []
        if hasattr(response, "source_nodes"):
            seen = set()
            for node in response.source_nodes:
                fname = node.metadata.get("file_name", "unknown")
                if fname not in seen:
                    sources.append(fname)
                    seen.add(fname)

        result = str(response)
        if sources:
            result += f"\n\nSources: {', '.join(sources)}"

        return result

    except Exception as e:
        return f"Error querying documents: {e}"
