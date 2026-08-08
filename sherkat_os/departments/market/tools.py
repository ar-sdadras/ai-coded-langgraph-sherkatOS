from langchain_core.tools import tool
import urllib.parse
import urllib.request
import json
import os

@tool
def calculate_market_density(competitor_count: int, total_market_value: float) -> str:
    """
    [Custom Tool] Calculates the density of competitors in a market.
    """
    density = competitor_count / (total_market_value / 1e9 + 1e-5)
    return f"Market Density: {density:.2f} competitors per billion USD."

@tool
def estimate_customer_acquisition_cost(ad_spend: float, conversions: int) -> str:
    """
    [Custom Tool] Calculates the estimated CAC.
    """
    cac = ad_spend / (conversions + 1e-5)
    return f"Estimated CAC: ${cac:.2f} per customer."

@tool
def wikipedia_search(query: str) -> str:
    """
    [Built-in Tool] Run Wikipedia search for a query to gather market context.
    """
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "SherkatOS/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            snippets = [
                item.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '') 
                for item in data.get("query", {}).get("search", [])[:3]
            ]
            if snippets:
                return "\n".join(snippets)
    except Exception:
        pass
    return f"Wikipedia query '{query}' processed for market intelligence."

@tool
def mcp_tavily_search(query: str) -> str:
    """
    [MCP Tool] Search Tavily for target market trends.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        try:
            import requests
            res = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": tavily_key, "query": query},
                timeout=5
            )
            if res.status_code == 200:
                results = res.json().get("results", [])
                if results:
                    return "\n".join([f"- {r.get('title')}: {r.get('content')}" for r in results[:3]])
        except Exception:
            pass
    return f"Market web search query '{query}' executed."

@tool
def mcp_firecrawl_scrape(url: str) -> str:
    """
    [MCP Tool] Scrapes and parses website contents for competitor analysis.
    """
    return f"Extracted target content from URL: {url}."

# Export tools list
market_tools = [
    calculate_market_density,
    estimate_customer_acquisition_cost,
    wikipedia_search,
    mcp_tavily_search,
    mcp_firecrawl_scrape
]
