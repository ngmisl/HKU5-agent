import json
import re
from typing import Any, Optional, cast

from pydantic import BaseModel, Field, model_validator
from smolagents import tool  # type: ignore


class VirusRiskAssessment(BaseModel):
    """Model for virus risk assessment data"""

    risk_level: int = Field(default=5, ge=1, le=10, description="Risk level from 1-10")
    transmission: str = Field(
        default="", description="Analysis of transmission potential"
    )
    mortality: str = Field(default="", description="Analysis of mortality rates")
    mutation: str = Field(default="", description="Analysis of mutation potential")
    containment: str = Field(default="", description="Analysis of containment status")
    treatment: str = Field(default="", description="Analysis of available treatments")
    summary: str = Field(default="", description="Brief explanation of overall risk")
    assessment_date: str = Field(
        default="", description="Date when assessment was made"
    )

    @model_validator(mode="after")
    def validate_risk_level(self) -> "VirusRiskAssessment":
        """Ensure risk level is between 1 and 10"""
        if hasattr(self, "risk_level"):
            self.risk_level = max(1, min(10, self.risk_level))
        return self

    @model_validator(mode="after")
    def check_fields_not_empty(self) -> "VirusRiskAssessment":
        """Ensure fields are not empty"""
        for field in self.model_fields:
            value = getattr(self, field)
            if isinstance(value, str) and not value:
                setattr(self, field, f"No data available for {field}")
        return self

    model_config = {"validate_assignment": True}


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

    # Define the expected schema using the Pydantic model
    schema = {
        "risk_level": "number between 1-10",
        "transmission": "analysis of transmission potential",
        "mortality": "analysis of mortality rates",
        "mutation": "analysis of mutation potential",
        "containment": "analysis of containment status",
        "treatment": "analysis of available treatments",
        "summary": "brief explanation of overall risk",
        "assessment_date": assessment_date,
    }

    schema_str = json.dumps(schema, indent=2)

    prompt = f"""Based on this information about {virus_name} (assessment date: {assessment_date}):
{current_data}

Please provide a risk assessment in JSON format using this structure:
{schema_str}

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

    # Define the expected schema using the Pydantic model
    schema = {
        "risk_level": "number between 1-10",
        "transmission": "analysis of transmission potential",
        "mortality": "analysis of mortality rates",
        "mutation": "analysis of mutation potential",
        "containment": "analysis of containment status",
        "treatment": "analysis of available treatments",
        "summary": "brief explanation of overall risk",
        "assessment_date": assessment_date,
    }

    schema_str = json.dumps(schema, indent=2)

    prompt = f"""Based on this information about H5N1 (Avian Influenza) (assessment date: {assessment_date}):
{current_data}

Please provide a risk assessment in JSON format using this structure:
{schema_str}

Make sure your response contains ONLY valid JSON that can be parsed directly. Do not include any markdown formatting, code block indicators, or explanatory text before or after the JSON.
"""

    return prompt


@tool
def clean_agent_response(response: str) -> dict[str, Any]:
    """
    Cleans up agent responses and extracts the structured JSON data.

    Args:
        response: The raw response from the agent containing risk assessment JSON

    Returns:
        A dictionary with cleaned and structured risk assessment data
    """
    # Default assessment data using Pydantic model
    default_assessment: dict[str, Any] = VirusRiskAssessment().model_dump()

    # Initial json extraction attempt
    extracted_json = extract_json_from_text(response)

    # Verify extracted_json is a proper dictionary with string keys
    if isinstance(extracted_json, dict) and all(
        isinstance(key, str) for key in extracted_json.keys()
    ):
        try:
            # Use Pydantic to validate and clean the data
            validated_assessment = VirusRiskAssessment(**extracted_json)
            return cast(dict[str, Any], validated_assessment.model_dump())
        except Exception as e:
            print(f"Validation error: {e}")

    # If JSON extraction failed, try the fallback approach with regex parsing
    cleaned_data = default_assessment.copy()
    current_field: Optional[str] = None

    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            parts = line.split(":", 1)
            field = parts[0].lower().strip()
            value = parts[1].strip() if len(parts) > 1 else ""

            # Map field names
            normalized_field = field.replace(" ", "_").lower()
            if normalized_field in cleaned_data:
                current_field = normalized_field

                if normalized_field == "risk_level":
                    try:
                        # Extract first number from value
                        numbers = re.findall(r"\d+", value)
                        if numbers:
                            cleaned_data[normalized_field] = int(numbers[0])
                    except (ValueError, IndexError):
                        pass
                else:
                    cleaned_data[normalized_field] = value
        elif current_field and current_field != "risk_level":
            if cleaned_data[current_field]:
                cleaned_data[current_field] += " " + line
            else:
                cleaned_data[current_field] = line

    # Validate with Pydantic one more time to ensure all constraints are met
    try:
        validated_assessment = VirusRiskAssessment(**cleaned_data)
        return cast(dict[str, Any], validated_assessment.model_dump())
    except Exception as e:
        print(f"Final validation error: {e}")
        return default_assessment


@tool
def extract_json_from_text(text: str) -> dict[str, Any]:
    """
    Attempts to extract JSON from text response, handling various formats.

    Args:
        text: Text that may contain JSON data

    Returns:
        Extracted JSON as a dictionary or empty dict if no valid JSON found
    """
    if not text:
        return {}

    # Try to find JSON pattern with matching braces
    json_pattern = re.compile(r"({[\s\S]*?})")
    matches = json_pattern.findall(text)

    for match in matches:
        try:
            json_data = json.loads(match)
            # Ensure we have a dictionary with string keys
            if isinstance(json_data, dict) and all(
                isinstance(key, str) for key in json_data.keys()
            ):
                return cast(dict[str, Any], json_data)
        except json.JSONDecodeError:
            continue

    # If that fails, try to find content between ```json and ``` markers
    code_block_pattern = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```")
    matches = code_block_pattern.findall(text)

    for match in matches:
        try:
            code_data = json.loads(match)
            # Ensure we have a dictionary with string keys
            if isinstance(code_data, dict) and all(
                isinstance(key, str) for key in code_data.keys()
            ):
                return cast(dict[str, Any], code_data)
        except json.JSONDecodeError:
            continue

    # Return empty dict if no valid JSON found
    return {}
