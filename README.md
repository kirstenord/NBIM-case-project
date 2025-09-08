# NBIM Dividend Reconciliation System

**LLM-Powered Automated Dividend Reconciliation**

A solution for automating NBIM's dividend reconciliation process using CrewAI agents powered by Claude Sonnet.

## Overview

This system addresses NBIM's challenge of reconciling 8,000+ annual dividend events between internal systems and global custodians. It uses AI agents to detect discrepancies, classify risks, and propose solutions.

## Architecture

```
src/
├── core/                    # Core reconciliation logic
│   ├── models.py           # Data models and types
│   └── reconciliation_engine.py  # Break detection engine
├── agents/                 # AI agents for analysis
│   └── dividend_agents.py  # CrewAI agent definitions
├── tools/                  # Utility functions
│   └── data_formatter.py   # Data formatting for agents
└── main.py                 # Main application entry point

tests/                      # Test files
data/                       # Sample dividend CSV files
```

## Key Components

### Core Reconciliation Engine
- Loads NBIM and custodian dividend data
- Detects discrepancies in amounts, dates, tax rates
- Classifies breaks by severity and financial impact

### AI Agents
- **Detective Agent**: Analyzes breaks with market expertise
- **Classifier Agent**: Assesses risk and prioritizes issues  
- **Resolver Agent**: Proposes specific solutions

### Sample Results
The system successfully identifies real discrepancies in sample data:
- Samsung event: 4 breaks including $450K net amount difference
- Apple event: Perfect reconciliation 
- Nestle event: Minor amount variations

## Setup

```bash
# Install dependencies
uv sync

# Configure API key (optional)
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Run system
uv run python main.py

# Run tests  
uv run python tests/test_reconciliation.py
```

## Requirements

- Python 3.11+
- Anthropic API key (optional, for AI analysis)
- Sample CSV files in `data/` directory

## Output

The system provides:
- Detailed break detection results
- Financial impact analysis
- Risk classification by severity
- AI-powered recommendations (when API key configured)

This demonstrates how LLMs can transform financial operations through intelligent automation with appropriate safety controls.