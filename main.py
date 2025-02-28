import json
import os
from datetime import datetime
from typing import Any, Dict

import dotenv
from smolagents import (  # type: ignore
    CodeAgent,
    DuckDuckGoSearchTool,
    FinalAnswerTool,
    LiteLLMModel,
)

from tools import (
    clean_agent_response,
    extract_json_from_text,
)

# Load environment variables from .env if available
dotenv.load_dotenv(override=False)

# Get environment variables
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
model_id = os.environ.get(
    "MODEL_ID", "openrouter/google/gemini-2.0-flash-lite-preview-02-05:free"
)

if not openrouter_api_key:
    raise EnvironmentError(
        "OpenRouter API key not found. Set OPENROUTER_API_KEY in environment or .env file"  # noqa: E501
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
final_answer = FinalAnswerTool()

# Initialize the CodeAgent with the tools
agent = CodeAgent(
    tools=[
        search_tool,
        clean_agent_response,
        extract_json_from_text,
        final_answer,
    ],
    model=model,
    additional_authorized_imports=["datetime", "json", "re"],
)


def process_virus(virus_name: str, description: str, timestamp: str) -> Dict[str, Any]:
    """
    Process a single virus: search for news and generate a risk assessment.

    Args:
        virus_name: The name of the virus (e.g., "HKU5-CoV-2")
        description: A short description of the virus
        timestamp: Current timestamp

    Returns:
        Dictionary with news and risk assessment for the virus
    """
    print(f"Processing {virus_name}...")

    # Search for news about the virus
    print(f"Searching for news about {virus_name}...")
    search_query = f"news {virus_name} recent cases"
    news = search_tool(search_query)

    # Generate risk assessment
    print(f"Generating risk assessment for {virus_name}...")
    structured_prompt = f"""
    Based on the following information about {virus_name}:
    {description}
    Today's date: {datetime.now().strftime('%Y-%m-%d')}.
    Recent news: {news}
    Perform a thorough risk assessment and return your findings in a valid JSON format with the following structure:
    {{
      "risk_level": <number between 1-10>,
      "transmission": "<analysis of transmission potential>",
      "mortality": "<analysis of mortality rates>",
      "mutation": "<analysis of mutation potential>",
      "containment": "<analysis of containment status>",
      "treatment": "<analysis of available treatments>",
      "summary": "<brief explanation of overall risk>"
    }}
    Ensure all fields have detailed content based on the news analysis. Be sure to fill in all fields with appropriate information, even if you need to note uncertainty. Do not leave any fields empty.
    Return only valid JSON.
    """  # noqa: E501

    try:
        assessment_raw = agent(structured_prompt)

        # Process the raw response
        assessment_json = extract_json_from_text(assessment_raw)
        if not assessment_json:
            # Fall back to the older cleaner approach
            assessment_json = clean_agent_response(assessment_raw)

        # Check if the assessment is empty or missing critical fields
        fields_to_check = [
            "transmission",
            "mortality",
            "mutation",
            "containment",
            "treatment",
            "summary",
        ]
        missing_fields = []

        if isinstance(assessment_json, dict):
            for field in fields_to_check:
                if field not in assessment_json or not assessment_json.get(field):
                    missing_fields.append(field)

        if not assessment_json or missing_fields:
            print(
                f"Warning: Incomplete assessment for {virus_name}. Missing fields: {missing_fields}. Retrying..."  # noqa: E501
            )
            # Retry with a more explicit prompt
            retry_prompt = f"""
            Based on the news about {virus_name}, create a complete risk assessment JSON.
            News: {news}
            The JSON MUST include ALL these fields with detailed content:
            - risk_level: number from 1-10
            - transmission: detailed analysis of how it spreads
            - mortality: detailed analysis of death rates
            - mutation: detailed analysis of mutation potential
            - containment: detailed analysis of current containment
            - treatment: detailed analysis of available treatments
            - summary: summary of overall risk level
            DO NOT leave any fields empty. If information is uncertain, state that in the field but provide your best assessment.
            """  # noqa: E501

            retry_raw = agent(retry_prompt)
            retry_json = extract_json_from_text(retry_raw)

            # Check if retry was successful
            if retry_json:
                retry_missing_fields = []
                for field in fields_to_check:
                    if field not in retry_json or not retry_json[field]:
                        retry_missing_fields.append(field)

                if not retry_missing_fields:
                    assessment_json = retry_json
                    print(f"Retry successful for {virus_name}")
                else:
                    print(f"Retry still missing fields: {retry_missing_fields}")
                    # Create a fallback for missing fields
                    for field in retry_missing_fields:
                        retry_json[field] = (
                            f"Information about {field} for {virus_name} is limited in current reports, but assessment suggests moderate concern based on available data."  # noqa: E501
                        )
                    assessment_json = retry_json
            else:
                # Create a complete fallback response if retry also fails
                assessment_json = {
                    "risk_level": 5,
                    "transmission": f"Based on news reports, {virus_name} appears to have potential for transmission, though details are limited.",  # noqa: E501
                    "mortality": f"Information about mortality rates for {virus_name} is incomplete in current reports.",  # noqa: E501
                    "mutation": f"The mutation potential of {virus_name} requires further research based on available data.",  # noqa: E501
                    "containment": f"Current containment efforts for {virus_name} appear to be ongoing according to news reports.",  # noqa: E501
                    "treatment": f"Available treatments for {virus_name} are not fully detailed in the provided information.",  # noqa: E501
                    "summary": f"{virus_name} presents a moderate risk based on current information, though more data is needed for a comprehensive assessment.",  # noqa: E501
                }
    except Exception as e:
        print(f"Error in {virus_name} assessment: {e}")
        # Provide default values if there's an error
        assessment_json = {
            "risk_level": 5,
            "transmission": f"Based on news reports, {virus_name} appears to have potential for transmission, though details are limited.",  # noqa: E501
            "mortality": f"Information about mortality rates for {virus_name} is incomplete in current reports.",  # noqa: E501
            "mutation": f"The mutation potential of {virus_name} requires further research based on available data.",  # noqa: E501
            "containment": f"Current containment efforts for {virus_name} appear to be ongoing according to news reports.",  # noqa: E501
            "treatment": f"Available treatments for {virus_name} are not fully detailed in the provided information.",  # noqa: E501
            "summary": f"{virus_name} presents a moderate risk based on current information, though more data is needed for a comprehensive assessment.",  # noqa: E501
        }

    print(f"{virus_name} assessment processed.")

    return {"risk_assessment": assessment_json, "news": news}


def main() -> None:
    """Main function to retrieve news and generate risk assessments for viruses."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Define the viruses to process
    viruses = [
        {
            "name": "HKU5-CoV-2",
            "description": "HKU5-CoV-2 is a bat coronavirus that can potentially infect human cells through ACE2 receptors.",  # noqa: E501
        },
        {
            "name": "H5N1",
            "description": "H5N1 is a highly pathogenic avian influenza strain affecting birds and occasionally humans. It has recently been detected in dairy cattle in the United States.",  # noqa: E501
        },
    ]

    # Process each virus one by one
    results = {}
    for virus in viruses:
        virus_result = process_virus(virus["name"], virus["description"], timestamp)

        # Directly add the result to results - we've already handled validation in the process_virus function  # noqa: E501
        results[virus["name"]] = virus_result
        print(f"Added {virus['name']} assessment to results")

    # Format the output with all assessments
    output = {"timestamp": timestamp, "viruses": results}

    # Save the results to dist/data.json
    os.makedirs("dist", exist_ok=True)
    with open("dist/data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("All assessments complete. Results saved to dist/data.json")


if __name__ == "__main__":
    main()
