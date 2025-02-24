from smolagents import tool  # type: ignore

@tool
def assess_virus_risk(virus_name: str, current_data: str, assessment_date: str) -> str:
    """
    Evaluates the current risk scenario of a virus based on provided data.

    Args:
        virus_name: Name of the virus to assess (e.g., "HKU5")
        current_data: Current information about the virus from news/research
        assessment_date: Date when this assessment is being made

    Returns:
        A string containing the risk assessment in the format:
        "Risk Level: X/10

        Detailed Assessment:
        - Transmission Rate: [description]
        - Mortality Rate: [description]
        - Mutation Risk: [description]
        - Containment Status: [description]
        - Treatment Availability: [description]"
    """
    # Analyze the data to determine risk factors
    if "SARS-CoV-2" in current_data and "receptor" in current_data:
        transmission_risk = "High potential - uses same receptor as SARS-CoV-2"
        transmission_score = 8
    else:
        transmission_risk = "Unknown - insufficient data on transmission mechanisms"
        transmission_score = 5

    if "no human cases" in current_data.lower():
        mortality_risk = "Unknown - no human cases reported yet"
        mortality_score = 5
        containment_status = "Currently contained - no human cases reported"
        containment_score = 2
    else:
        mortality_risk = "Unknown - data on human cases pending"
        mortality_score = 6
        containment_status = "Status unclear - monitoring required"
        containment_score = 6

    if "MERS" in current_data:
        mutation_risk = "High - belongs to merbecovirus subgenus like MERS"
        mutation_score = 7
    else:
        mutation_risk = "Unknown - insufficient data on viral genetics"
        mutation_score = 5

    if "coronavirus treatments" in current_data.lower():
        treatment_risk = "Limited - existing coronavirus treatments may be applicable"
        treatment_score = 4
    else:
        treatment_risk = "None available - specific treatments not yet developed"
        treatment_score = 8

    # Calculate weighted risk level
    weights = {
        'transmission': 0.3,
        'mortality': 0.2,
        'mutation': 0.2,
        'containment': 0.2,
        'treatment': 0.1
    }

    risk_level = round(
        transmission_score * weights['transmission'] +
        mortality_score * weights['mortality'] +
        mutation_score * weights['mutation'] +
        containment_score * weights['containment'] +
        treatment_score * weights['treatment']
    )

    # Format the response
    response = f"""Risk Level: {risk_level}/10

Detailed Assessment:
- Transmission Rate: {transmission_risk}
- Mortality Rate: {mortality_risk}
- Mutation Risk: {mutation_risk}
- Containment Status: {containment_status}
- Treatment Availability: {treatment_risk}

Risk Level Explanation:
{risk_level}/10 - Risk assessment based on:
1. Transmission potential: {transmission_score}/10 (30% weight)
2. Mortality uncertainty: {mortality_score}/10 (20% weight)
3. Mutation risk: {mutation_score}/10 (20% weight)
4. Current containment: {containment_score}/10 (20% weight)
5. Treatment options: {treatment_score}/10 (10% weight)

This assessment is dynamic and will be updated as new information becomes available."""

    return response
