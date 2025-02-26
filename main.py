from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool  # type: ignore
import dotenv
import os
import json
from datetime import datetime
from tools import assess_virus_risk, assess_h5n1_risk  # using the provided tools.py functions

# Load environment variables from .env if available
dotenv.load_dotenv(override=False)

# Get environment variables
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
model_id = os.environ.get(
    "MODEL_ID", "openrouter/google/gemini-2.0-flash-lite-preview-02-05:free"
)

if not openrouter_api_key:
    raise EnvironmentError(
        "OpenRouter API key not found. Set OPENROUTER_API_KEY in environment or .env file"
    )

# Initialize the model with OpenRouter configuration
model = LiteLLMModel(
    model_id=model_id,
    api_base="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
    num_ctx=8192,
)

# Initialize the DuckDuckGo search tool
search_tool = DuckDuckGoSearchTool()

# Initialize the CodeAgent with the tools (including our risk assessment tools)
agent = CodeAgent(
    tools=[search_tool, assess_virus_risk, assess_h5n1_risk],
    model=model,
)

def extract_content(agent_response: str) -> str:
    """Extracts and cleans response text from the agent."""
    lines = []
    for line in agent_response.split('\n'):
        line = line.strip()
        if line and not line.startswith('The date is'):
            lines.append(line)
    return "\n".join(lines)

def main() -> None:
    """Main function to retrieve news and generate risk assessments for HKU5 and H5N1."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Explicitly search for news on each virus
    print("Searching for news about HKU5...")
    hku5_news = search_tool("news HKU5")
    print("Searching for news about H5N1...")
    h5n1_news = search_tool("news H5N1")

    # Generate HKU5 risk assessment using the assess_virus_risk tool
    print("Generating HKU5 risk assessment...")
    hku5_prompt = assess_virus_risk(
        "HKU5",
        f"HKU5 is a bat coronavirus that can potentially infect human cells through ACE2 receptors. Recent news: {hku5_news}",
        timestamp,
    )
    hku5_assessment = extract_content(agent(hku5_prompt))

    # Generate H5N1 risk assessment using the assess_h5n1_risk tool
    print("Generating H5N1 risk assessment...")
    h5n1_prompt = assess_h5n1_risk(
        f"H5N1 is a highly pathogenic avian influenza strain affecting birds and occasionally humans. Recent news: {h5n1_news}",
        timestamp,
    )
    h5n1_assessment = extract_content(agent(h5n1_prompt))

    # Format the output with the assessments and news snippets
    output = {
        "timestamp": timestamp,
        "viruses": {
            "HKU5": {"risk_assessment": hku5_assessment, "news": hku5_news},
            "H5N1": {"risk_assessment": h5n1_assessment, "news": h5n1_news},
        },
    }

    # Save the results to dist/data.json
    os.makedirs("dist", exist_ok=True)
    with open("dist/data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Assessment complete. Results saved to dist/data.json")

if __name__ == "__main__":
    main()
