# first step - loading all the libraries

from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print


# =========================
# WEATHER TOOL
# =========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    print("[yellow]DEBUG WEATHER:[/yellow]", data)

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# =========================
# NEWS TOOL
# =========================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get latest news of a city"""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:

        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n{url}\n{snippet[:100]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# =========================
# TEST TOOLS
# =========================

print(get_weather.invoke("Bhopal"))
print(get_news.invoke("Bhopal"))


# =========================
# LLM
# =========================

llm = ChatMistralAI(
    model="mistral-small-2506"
)

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

llm_with_tools = llm.bind_tools(
    [get_weather, get_news]
)


# =========================
# AGENT LOOP
# =========================

messages = []

print("\n[bold green]City Intelligence System[/bold green]")
print("Type 'exit' to quit\n")


while True:

    user_input = input("You : ")

    if user_input.lower() == "exit":
        break

    messages.append(
        HumanMessage(content=user_input)
    )

    while True:

        result = llm_with_tools.invoke(messages)

        messages.append(result)

        # =========================
        # TOOL CALL REQUIRED
        # =========================

        if result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                print(
                    f"\n[cyan]Agent wants to call:[/cyan] {tool_name}"
                )

                confirm = input(
                    "Approve tool call? (yes/no): "
                )

                if confirm.lower() != "yes":
                    print("[red]Tool call denied[/red]")
                    continue

                # Execute tool

                tool_args = tool_call["args"]

                tool_result = tools[tool_name].invoke(tool_args)

                print("\n[green]TOOL OUTPUT:[/green]")
                print(tool_result)

                # Send tool result back to LLM

                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call["id"]
                    )
                )

            # Run agent again after tool execution
            continue

        # =========================
        # FINAL RESPONSE
        # =========================

        else:

            print("\n[bold magenta]Final Answer:[/bold magenta]\n")

            print(result.content)

            print("\n" + "=" * 60 + "\n")

            break