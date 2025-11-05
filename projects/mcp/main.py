from fastmcp import FastMCP

# サーバー名は用途が分かるように
mcp = FastMCP("OpenSearch Hybrid Search MCP")


@mcp.tool
def greet(name: str) -> str:
    """動作確認用の挨拶ツール。"""
    return f"Hello, {name}!"


@mcp.tool
def search(
    query: str,
    k: int = 50,
    size: int = 20,
):
    """
    OpenSearchのハイブリッド検索を実行します。

    引数:
    - query: 検索ワード（自然文）
    - k: ベクトル検索で取得する件数（デフォルト: 50）
    - size: 返却件数（デフォルト: 20）

    戻り値: ドキュメント(_source)の配列
    """
    # 依存を直に読み込んで実行（scripts/sample_code.py は使わない）
    from config.settings import Settings
    from services.opensearch_service import hybrid_search

    settings = Settings()
    result = hybrid_search(
        openai_api_key=settings.openai_api_key,
        openai_base_url=settings.openai_base_url,
        openai_embedding_model=settings.openai_embedding_model,
        openai_max_retries=settings.openai_max_retries,
        opensearch_base_url=settings.opensearch_base_url,
        opensearch_index_name=settings.opensearch_default_index_name,
        query=query,
        k=k,
        size=size,
    )
    hits = (result.get("hits") or {}).get("hits") or []
    return [h.get("_source") for h in hits[:size] if isinstance(h.get("_source"), dict)]


if __name__ == "__main__":
    mcp.run()
