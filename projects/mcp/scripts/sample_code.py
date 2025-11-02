from typing import Any, Dict, List, Type, Union


from services.opensearch_service import hybrid_search
from config.settings import Settings


def opensearch(
    question: str,
    k: int = 3,
    size: int = 3,
) -> List[Dict[str, Any]]:

    settings = Settings()
    result = hybrid_search(
        openai_api_key=settings.openai_api_key,
        openai_base_url=settings.openai_base_url,
        openai_embedding_model=settings.openai_embedding_model,
        openai_max_retries=settings.openai_max_retries,
        opensearch_base_url=settings.opensearch_base_url,
        opensearch_index_name=settings.opensearch_default_index_name,
        question=question,
        k=k,
        size=size,
    )
    hits = (result.get("hits") or {}).get("hits") or []
    return [h["_source"] for h in hits[:size] if isinstance(h.get("_source"), dict)]


if __name__ == "__main__":
    question = "キアヌについて教えて"
    result = opensearch(
        question=question,
        k=3,
        size=3,
    )

    print(result)
