import json
import re
from typing import Any, Dict

from smolagents import tool  # type: ignore


@tool
def assess_virus_risk(virus_name: str, current_data: str, assessment_date: str) -> str:
    """
    Summarizes current information about a virus from news/research data.

    Args:
        virus_name: Name of the virus to assess (e.g., "HKU5")
        current_data: Current information about the virus from news/research
        assessment_date: Date when this assessment is being made

    Returns:
        A summary of the current virus situation and key findings
    """
    if not current_data:
        return "No current data available for analysis."

    prompt = f"""Based on this information about {virus_name}:
{current_data}

Please provide a risk assessment in JSON format using this structure:
{{
  "risk_level": <number between 1-10>,
  "transmission": "<analysis of transmission potential>",
  "mortality": "<analysis of mortality rates>",
  "mutation": "<analysis of mutation potential>",
  "containment": "<analysis of containment status>",
  "treatment": "<analysis of available treatments>",
  "summary": "<brief explanation of overall risk>"
}}

Make sure your response contains ONLY valid JSON that can be parsed directly. Do not include any markdown formatting, code block indicators, or explanatory text before or after the JSON.
"""

    return prompt


@tool
def assess_h5n1_risk(current_data: str, assessment_date: str) -> str:
    """
    Summarizes current information about H5N1 from news/research data.

    Args:
        current_data: Current information about H5N1 from news/research
        assessment_date: Date when this assessment is being made

    Returns:
        A summary of the current H5N1 situation and key findings
    """
    if not current_data:
        return "No current data available for analysis."

    prompt = f"""Based on this information about H5N1 (Avian Influenza):
{current_data}

Please provide a risk assessment in JSON format using this structure:
{{
  "risk_level": <number between 1-10>,
  "transmission": "<analysis of transmission potential>",
  "mortality": "<analysis of mortality rates>",
  "mutation": "<analysis of mutation potential>",
  "containment": "<analysis of containment status>",
  "treatment": "<analysis of available treatments>",
  "summary": "<brief explanation of overall risk>"
}}

Make sure your response contains ONLY valid JSON that can be parsed directly. Do not include any markdown formatting, code block indicators, or explanatory text before or after the JSON.
"""

    return prompt


@tool
def clean_agent_response(response: str) -> Dict[str, Any]:
    """
    Cleans up agent responses and extracts the structured JSON data.

    Args:
        response: The raw response from the agent containing risk assessment JSON

    Returns:
        A dictionary with cleaned and structured risk assessment data
    """
    # Initialize with default values
    default_data = {
        "risk_level": 5,
        "transmission": "",
        "mortality": "",
        "mutation": "",
        "containment": "",
        "treatment": "",
        "summary": "",
    }

    # Try to extract just the JSON portion from the response
    try:
        # Find JSON-like content between curly braces
        json_match = re.search(r"({[\s\S]*})", response)
        if json_match:
            json_str = json_match.group(1)
            # Parse the JSON
            parsed_data = json.loads(json_str)

            # Make sure all expected fields are present
            for key in default_data:
                if key not in parsed_data:
                    parsed_data[key] = default_data[key]

            # Ensure risk_level is an integer between 1-10
            if "risk_level" in parsed_data:
                try:
                    risk_level = int(parsed_data["risk_level"])
                    parsed_data["risk_level"] = max(1, min(10, risk_level))
                except (ValueError, TypeError):
                    parsed_data["risk_level"] = default_data["risk_level"]

            return parsed_data

    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing JSON: {e}")

    # If we failed to parse JSON, try the old approach
    cleaned_data = default_data.copy()
    current_field = None

    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            parts = line.split(":", 1)
            field = parts[0].lower().strip()
            value = parts[1].strip() if len(parts) > 1 else ""

            # Map field names
            if field == "risk_level":
                try:
                    # Extract first number from value
                    numbers = re.findall(r"\d+", value)
                    if numbers:
                        cleaned_data["risk_level"] = min(max(1, int(numbers[0])), 10)
                except (ValueError, IndexError):
                    pass
            elif field in cleaned_data:
                current_field = field
                cleaned_data[current_field] = value
        elif current_field and current_field != "risk_level":
            if cleaned_data[current_field]:
                cleaned_data[current_field] += " " + line
            else:
                cleaned_data[current_field] = line

    return cleaned_data


@tool
def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Attempts to extract JSON from text response, handling various formats.

    Args:
        text: Text that may contain JSON data

    Returns:
        Extracted JSON as a dictionary or empty dict if no valid JSON found
    """
    # Try to find JSON pattern with matching braces
    json_pattern = re.compile(r"({[\s\S]*})")
    match = json_pattern.search(text)

    if match:
        try:
            json_str = match.group(1)
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    # If that fails, try to find content between ```json and ``` markers
    code_block_pattern = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```")
    match = code_block_pattern.search(text)

    if match:
        try:
            json_str = match.group(1)
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    # Return empty dict if no valid JSON found
    return {}
