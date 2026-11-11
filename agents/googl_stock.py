import requests
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

NAME = "googl-stock"


def fetch_googl():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GOOGL?interval=1d&range=1d"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()

    meta = r.json()["chart"]["result"][0]["meta"]
    price = meta["regularMarketPrice"]
    prev = meta["chartPreviousClose"]
    change = price - prev
    pct = (change / prev) * 100 if prev else 0

    return {
        "symbol": "GOOGL",
        "price": round(price, 2),
        "previous_close": round(prev, 2),
        "change": round(change, 2),
        "pct_change": round(pct, 2),
    }


def run():

    data = fetch_googl()

    agent = create_agent(
        model=ChatOllama(model="qwen2.5:7b", temperature=0),
        tools=[],
        system_prompt=(
            "You write short stock summaries. "
            "Given stock data, write 2 concise Markdown bullet points explaining "
            "the price move and whether it was an up or down day."
        ),
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": str(data)}]
    })

    return (
        "# GOOGL Daily Summary\n\n"
        f"{result['messages'][-1].content}\n\n"
        f"**Raw data:** `{data}`\n"
    )