from langchain_core.tools import tool

@tool
def calculate_market_density(competitor_count: int, total_market_value: float) -> str:
    """
    [Custom Tool] Calculates the density of competitors in a market.
    """
    density = competitor_count / (total_market_value / 1e9 + 1e-5)
    return f"Calculated Market Density: {density:.2f} competitors per billion USD."

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
    [Built-in Tool] Run Wikipedia search for a query.
    """
    return f"Wikipedia Search Result: '{query}' is widely adopted in AI corporate workflow architectures."

@tool
def mcp_tavily_search(query: str) -> str:
    """
    [MCP Tool: mcp-docker-toolkit/tavily_search] Search Tavily for target market trends.
    """
    return f"Tavily Search: Found 12 fast-growing SaaS startups specializing in LangGraph multi-agent simulation."

@tool
def mcp_firecrawl_scrape(url: str) -> str:
    """
    [MCP Tool: mcp-docker-toolkit/firecrawl_scrape] Scrapes and parses website contents.
    """
    return f"Firecrawl Scraped: Successfully parsed competitor features showing slow state transitions."

# Export tools list
market_tools = [
    calculate_market_density,
    estimate_customer_acquisition_cost,
    wikipedia_search,
    mcp_tavily_search,
    mcp_firecrawl_scrape
]
