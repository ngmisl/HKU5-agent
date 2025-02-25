from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool  # type: ignore
import dotenv
import os
import json
from datetime import datetime
from tools import assess_virus_risk, assess_h5n1_risk, format_risk_assessment

# Try to load .env if it exists, but don't fail if it doesn't
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

# Initialize model with OpenRouter configuration
model = LiteLLMModel(
    model_id=model_id,
    api_base="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
    num_ctx=8192,
)

# Initialize tools
search_tool = DuckDuckGoSearchTool(timeout=10)
agent = CodeAgent(
    tools=[search_tool, assess_virus_risk, assess_h5n1_risk, format_risk_assessment],
    model=model,
)


def extract_content(agent_response: str) -> str:
    """Extract content from agent response"""
    # Clean up any trailing newlines or extra whitespace
    lines = []
    for line in agent_response.split('\n'):
        line = line.strip()
        if line and not line.startswith('The date is'):
            lines.append(line)
    return '\n'.join(lines)


def main() -> None:
    """Main function to generate virus risk assessment"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate risk assessments
    print("Generating HKU5 assessment...")
    hku5_assessment = extract_content(
        agent(
            format_risk_assessment(
                "HKU5",
                "HKU5 is a bat coronavirus that can potentially infect human cells through ACE2 receptors.",
                timestamp,
            )
        )
    )

    print("Generating H5N1 assessment...")
    h5n1_assessment = extract_content(
        agent(
            format_risk_assessment(
                "H5N1",
                "H5N1 is a highly pathogenic avian influenza strain affecting birds and occasionally humans.",
                timestamp,
            )
        )
    )

    # Format output
    output = {
        "timestamp": timestamp,
        "viruses": {
            "HKU5": {"risk_assessment": hku5_assessment},
            "H5N1": {"risk_assessment": h5n1_assessment},
        },
    }

    # Save to file
    os.makedirs("dist", exist_ok=True)
    with open("dist/data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Assessment complete. Results saved to dist/data.json")


if __name__ == "__main__":
    main()
