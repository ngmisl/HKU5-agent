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

Please provide a concise summary of the key findings and current situation, including:
- Major developments
- Geographic spread
- Notable incidents or outbreaks
- Current research status
- Public health measures

The date is {assessment_date}"""

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

Please provide a concise summary of the key findings and current situation, including:
- Major developments in human and animal cases
- Geographic spread and affected populations
- Notable outbreaks or clusters
- Current research and surveillance efforts
- Public health measures and recommendations

The date is {assessment_date}"""

    return prompt

@tool
def format_risk_assessment(virus_name: str, summary_data: str, assessment_date: str) -> Dict[str, Any]:
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

Analyze the data and provide a risk assessment in exactly this format:
RISK_LEVEL: [number between 1-10]
TRANSMISSION: [detailed analysis of transmission potential and patterns]
MORTALITY: [analysis of known or potential mortality rates]
MUTATION: [analysis of genetic changes and adaptation potential]
CONTAINMENT: [evaluation of current containment measures]
TREATMENT: [status of available treatments and vaccines]
SUMMARY: [brief explanation of the overall risk assessment]

The date is {assessment_date}"""

    return prompt
