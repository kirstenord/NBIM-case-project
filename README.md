# NBIM Dividend Reconciliation System

**AI-Powered Multi-Agent System for Financial Reconciliation**

An intelligent reconciliation system using CrewAI's multi-agent framework to automate dividend payment validation between NBIM and custodian records.

## 📌 The Challenge

NBIM processes ~8,000 dividend events annually across 9,000+ equity holdings. Daily reconciliation between internal systems and global custodians is time-consuming and error-prone. This project explores how LLMs can transform this workflow through intelligent automation.

## 🚀 Quick Start

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/kirstenord/nbim-case-project.git
cd nbim-case-project
uv sync

# Configure API key
echo "ANTHROPIC_API_KEY=your_claude_api_key_here" > .env

# Run reconciliation
uv run streamlit run main.py
```

## 🏗️ Architecture

**8 Specialized Agents** working sequentially to analyze dividend data:

1. **Data Detective** (CSV Data Parser & Matcher) - Parses CSVs and matches records by COAC_EVENT_KEY
2. **Math Calculator** (Currency-Aware Amount Calculator) - Calculates differences preserving original currencies
3. **Position Validator** - Verifies share quantities and identifies position mismatches
4. **Tax Analyst** (Tax Rate Specialist) - Analyzes tax rates and identifies treaty opportunities
5. **Securities Lending Checker** (Securities Lending Analyst) - Analyzes lending impact on tax efficiency
6. **FX Validator** (FX Rate Validator) - Validates FX rates and detects pricing issues
7. **Risk Prioritizer** (Risk Assessor) - Prioritizes discrepancies by financial impact
8. **Report Writer** (Report Synthesizer) - Synthesizes all analyses into executive reports

## 📁 Project Structure

```
src/crews/
├── config/
│   ├── agents.yaml    # Agent roles and personas
│   └── tasks.yaml     # Task workflows (prompts)
├── crew.py            # CrewAI orchestration
└── main.py            # Entry point
```

## 📋 Deliverables

✅ **Working Prototype** - Processes test data with LLM integration  
✅ **Architecture Vision** - Scalable 8-agent system design  
✅ **Analysis & Recommendations** - Risk assessment and recommendations

See [architecture.md](architecture.md) and [analysis_and_recommendations.md](analysis_and_recommendations.md) for details.


## 🔧 Configuration

- **LLM**: Claude Sonnet 4.0

---
