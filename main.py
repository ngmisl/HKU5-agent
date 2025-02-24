from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool  # type: ignore
import dotenv
import os
from datetime import datetime
from tools import assess_virus_risk

dotenv.load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
model_id = os.getenv("MODEL_ID", "openrouter/google/gemini-2.0-flash-lite-preview-02-05:free")

if not openrouter_api_key:
    raise EnvironmentError(
        "OpenRouter API key not found. Set OPENROUTER_API_KEY in .env"
    )

model = LiteLLMModel(
    model_id=model_id,
    api_base="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
    num_ctx=8192,
)

# Initialize tools
search_tool = DuckDuckGoSearchTool()
agent = CodeAgent(
    tools=[search_tool, assess_virus_risk], model=model, add_base_tools=True
)

# Search for latest HKU5 news
search_results = search_tool("news HKU5")[:5]  # Get the latest 5 results

# Debug: Print raw search results
print("Search Results:")
for i, result in enumerate(search_results, 1):
    print(f"\n--- Result {i} ---")
    print(result)
print("\n-------------------\n")

# Only proceed with summary if we have results
if search_results:
    # Format the search results for the AI to summarize
    news_text = "\n\n".join(search_results)
    current_date = datetime.now()

    # First get a summary
    summary_prompt = f"""Today is {current_date.strftime('%Y-%m-%d')}. Here are the latest search results about HKU5 coronavirus. Please provide a concise summary of the key points:

{news_text}

Please summarize the main findings and developments regarding HKU5 from these sources and add the date."""

    summary = agent.run(summary_prompt)
    print("\nHKU5 Research Summary:")
    print(summary)

    # Use the risk assessment tool
    risk_prompt = f"""Use the assess_virus_risk tool to evaluate HKU5 based on this information:
{summary}

The date is {current_date.strftime('%m/%d/%y %H:%M:%S')}"""

    risk_result = agent.run(risk_prompt)
    print(f"\nSummary: {summary}")
    print(f"\nRisk Assessment Results: {risk_result}")

else:
    print("No search results found for HKU5. Try modifying the search terms.")
