# HKU5 Risk Assessment Tool

A Python-based tool that monitors and assesses the risk level of the HKU5 coronavirus using AI-powered analysis of the latest research and news. The tool uses OpenRouter.ai's free models (like Google's Gemini) to provide detailed risk assessments and summaries.

## Features

- Real-time news gathering using DuckDuckGo search
- AI-powered summarization of research findings
- Detailed virus risk assessment with multiple factors
- Risk scoring on a scale of 1-10
- Uses free AI models through OpenRouter.ai

## Prerequisites

1. Install uv (fast Python package installer):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hku5-risk-assessment.git
cd hku5-risk-assessment
```

2. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Copy example.env to .env and fill in your API keys:

```bash
cp example.env .env
```

## Configuration

Edit your `.env` file with the following settings:

```env
# Required: Your OpenRouter API key
OPENROUTER_API_KEY=your-openrouter-api-key-here

# Required: The model ID to use for AI interactions
MODEL_ID="openrouter/google/gemini-2.0-flash-lite-preview-02-05:free"

# Optional: Your site URL for attribution
OR_SITE_URL="https://your-site-url.com"

# Optional: Your application name for attribution
OR_APP_NAME="Your App Name"
```

## Usage

Run the main script:

```bash
python main.py
```

## Example Output

```txt
Summary: As of 2025-02-24, research has identified a new bat coronavirus, HKU5-CoV-2, in China. It shares similarities with the virus that causes COVID-19, including the ability to enter human cells using the ACE2 receptor.  It belongs to the merbecovirus subgenus, like MERS. While no human cases have been reported, the potential for transmission is high. The risk assessment is high due to the shared ACE2 usage and relation to MERS. Preparedness is crucial.

Risk Assessment Results: Risk Level: 6/10

Detailed Assessment:
- Transmission Rate: High potential - uses same receptor as SARS-CoV-2
- Mortality Rate: Unknown - no human cases reported yet
- Mutation Risk: High - belongs to merbecovirus subgenus like MERS
- Containment Status: Currently contained - no human cases reported
- Treatment Availability: Limited - existing coronavirus treatments may be applicable

Risk Level Explanation:
6/10 - High risk due to:
1. Uses same receptor as SARS-CoV-2, indicating high potential for human transmission
2. Related to MERS virus, suggesting potential severity
3. No human cases yet, but preparedness is crucial
4. Existing coronavirus treatments might help but specific treatments not yet developed
```

## AI Model

This tool uses OpenRouter.ai's free tier, which provides access to various AI models including Google's Gemini. The model can be configured through the `MODEL_ID` environment variable.

Current supported free models through OpenRouter include:

- openrouter/google/gemini-2.0-flash-lite-preview-02-05:free
- Other free models available at [OpenRouter's model list](https://openrouter.ai/models)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this code for any purpose.

## Disclaimer

This tool provides risk assessments based on available public information and AI analysis. Always consult health authorities and medical professionals for official guidance.
