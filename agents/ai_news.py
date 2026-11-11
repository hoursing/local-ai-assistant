from ddgs import DDGS
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

NAME = "ai-news"

def search_ai_news(query: str = "latest artificial intelligence news Oct 2026") -> str:
    """
    Tìm kiếm các tin tức mới nhất về trí tuệ nhân tạo trên internet.
    
    Args:
        query: Từ khóa tìm kiếm tin tức.
    """
    print(f"\n[Agent đang gọi Tool] Đang tìm kiếm với từ khóa: '{query}'...")
    results = []
    try:
        # Sử dụng DuckDuckGo để tìm kiếm mà không cần API Key phức tạp
        with DDGS() as ddg:
            for r in ddg.text(query, max_results=5):
                results.append({
                    "title": r.get("title"),
                    "href": r.get("href"),
                    "body": r.get("body")
                })
    except Exception as e:
        return f"Lỗi khi tìm kiếm: {str(e)}"

    return results;


def run():
    results = search_ai_news()

    agent = create_agent(
        model=ChatOllama(model="qwen2.5:7b", temperature=0),
        tools=[],
        system_prompt=(
            "You write short AI news digests. "
            "Given search results, produce 3-5 Markdown bullet points. "
            "Each bullet should summarize one important story and end with its source URL."
        ),
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": str(results)}]
    })

    return f"# Daily AI News Digest\n\n{result['messages'][-1].content}\n"