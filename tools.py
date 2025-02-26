from smolagents import tool  # type: ignore
from typing import Dict, Any


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

Please provide a risk assessment in this exact format:
RISK_LEVEL: [number between 1-10]
TRANSMISSION: [analysis of transmission potential]
MORTALITY: [analysis of mortality rates]
MUTATION: [analysis of mutation potential]
CONTAINMENT: [analysis of containment status]
TREATMENT: [analysis of available treatments]
SUMMARY: [brief explanation of overall risk]"""

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

Please provide a risk assessment in this exact format:
RISK_LEVEL: [number between 1-10]
TRANSMISSION: [analysis of transmission potential]
MORTALITY: [analysis of mortality rates]
MUTATION: [analysis of mutation potential]
CONTAINMENT: [analysis of containment status]
TREATMENT: [analysis of available treatments]
SUMMARY: [brief explanation of overall risk]"""

    return prompt


@tool
def format_risk_assessment(
    virus_name: str, summary_data: str, assessment_date: str
) -> Dict[str, Any]:
    """
    Formats a risk assessment based on summarized virus data.

    Args:
        virus_name: Name of the virus (e.g., "HKU5" or "H5N1")
        summary_data: Summarized information about the virus
        assessment_date: Date of the assessment

    Returns:
        A dictionary containing the formatted risk assessment with all required fields
    """
    prompt = f"""Based on this summary about {virus_name}:
{summary_data}

Please provide a risk assessment in this exact format:
RISK_LEVEL: [number between 1-10]
TRANSMISSION: [analysis of transmission potential]
MORTALITY: [analysis of mortality rates]
MUTATION: [analysis of mutation potential]
CONTAINMENT: [analysis of containment status]
TREATMENT: [analysis of available treatments]
SUMMARY: [brief explanation of overall risk]"""

    return prompt


@tool
def clean_agent_response(response: str) -> Dict[str, Any]:
    """
    Cleans up agent responses and extracts the structured risk assessment data.

    Args:
        response: The raw response from the agent containing risk assessment

    Returns:
        A dictionary with cleaned and structured risk assessment data
    """
    # Initialize with empty strings
    cleaned_data = {
        "risk_level": 5,  # Default risk level
        "transmission": "",
        "mortality": "",
        "mutation": "",
        "containment": "",
        "treatment": "",
        "summary": ""
    }

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
                    import re
                    numbers = re.findall(r'\d+', value)
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
