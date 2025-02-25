[![CodeQL](https://github.com/ngmisl/HKU5-agent/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ngmisl/HKU5-agent/actions/workflows/github-code-scanning/codeql) [![Daily Update and Deploy](https://github.com/ngmisl/HKU5-agent/actions/workflows/daily-update.yml/badge.svg)](https://github.com/ngmisl/HKU5-agent/actions/workflows/daily-update.yml)

# Virus Risk Dashboard

Real-time risk assessment dashboard for emerging viral threats, focusing on HKU5 and H5N1 viruses.

## Features

- Daily automated risk assessments using AI analysis
- Clean, modern dashboard interface
- Real-time data updates
- Mobile-responsive design

## Setup

1. Create the following repository secrets in GitHub:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `MODEL_ID`: The model ID to use (default: openrouter/google/gemini-2.0-flash-lite-preview-02-05:free)
   - `OR_SITE_URL`: Your site URL
   - `OR_APP_NAME`: Your app name
   - `ORBITER_API_KEY`: Your Orbiter API key

2. The GitHub Action will:
   - Run daily at 00:00 UTC
   - Generate fresh risk assessments
   - Deploy updates to Orbiter automatically

## Local Development

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the script
uv run main.py
```

## Disclaimer

This dashboard uses AI to generate risk assessments. The AI may hallucinate or provide inaccurate information. Always verify critical information with official sources.
