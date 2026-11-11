import requests
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

NAME = "weather-brief"


def fetch_weather():
    r = requests.get("https://wttr.in/Da+Nang?format=j1", timeout=15)
    r.raise_for_status()

    current = r.json()["current_condition"][0]
    return {
        "temp_f": current["temp_F"],
        "feels_like_f": current["FeelsLikeF"],
        "humidity": current["humidity"],
        "wind_mph": current["windspeedMiles"],
        "description": current["weatherDesc"][0]["value"],
    }


def run():
    weather = fetch_weather()

    agent = create_agent(
        model=ChatOllama(model="qwen2.5:7b", temperature=0),
        tools=[],
        system_prompt=(
            "You write short weather briefs. "
            "Given current weather data, write 2 concise Markdown bullet points "
            "summarizing the conditions in plain English."
        ),
    )

    result = agent.invoke({
        "messages": [{"role": "user", "content": str(weather)}]
    })

    return f"# Daily Weather Brief\n\n{result['messages'][-1].content}\n"