# System Architecture

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT DATA                              │
│            NBIM Records  +  Custody Records                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    8-AGENT PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DATA DETECTIVE                                              │
│           ↓                                                     │
│  2. MATH CALCULATOR                                             │
│           ↓                                                     │
│  3. POSITION VALIDATOR                                          │
│           ↓                                                     │
│  4. TAX ANALYST                                                 │
│           ↓                                                     │
│  5. SECURITIES LENDING CHECKER                                  │
│           ↓                                                     │
│  6. FX VALIDATOR                                                │
│           ↓                                                     │
│  7. RISK PRIORITIZER                                            │
│           ↓                                                     │
│  8. REPORT WRITER                                               │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RECONCILIATION REPORT                       │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Architecture

```
                        ┌─────────────────┐
                        │ Claude Sonnet   │
                        │     4.0 LLM     │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ agents.yaml  │        │ tasks.yaml   │        │   crew.py    │
│              │        │              │        │              │
│ Defines:     │        │ Defines:     │        │ Orchestrates:│
│ • Roles      │        │ • Workflows  │        │ • Sequential │
│ • Goals      │        │ • Prompts    │        │   execution  │
│ • Personas   │        │ • Outputs    │        │ • Context    │
└──────────────┘        └──────────────┘        └──────────────┘

CONTEXT FLOW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stage 1: DATA DETECTIVE
         Input: Raw CSV data
         Output: Matched records → Creates base context
                               ↓
Stage 2: VALIDATORS (receive Data Detective's context)
         ├─ Math Calculator: Calculates differences
         ├─ Position Validator: Verifies shares  
         ├─ Tax Analyst: Analyzes rates
         ├─ Securities Lending: Checks lending
         └─ FX Validator: Validates rates
                               ↓
Stage 3: RISK PRIORITIZER
         Input: ALL validator contexts
         Output: Prioritized issues
                               ↓
Stage 4: REPORT WRITER
         Input: Complete context chain
         Output: Executive report
```

## My Approach


I had never used the CrewAI Framework before, but knew it was good for multi-agent architectures. I first began reading the CrewAI documentation to try to understand how everything works together. From there, I tried to build a super simple proof of concept. I followed the recommendations provided in the documentation: configuring agents and tasks with YAML configuration. 

As my confidence increased, I produced more agents and specified their tasks. Most of my time went to prompt engineering. The challenge with this project is that I have not been involved in dividend reconciliation before, so crafting an agentic system meant to automate this process was difficult. Many of the task descriptions are based on my own understanding of what is done during this process. The good thing about agentic systems is that changing the prompts is a simple thing to do - business experts can refine the YAML configurations without touching the code.

**Key Challenges & Solutions:**
- **Challenge**: Understanding what each reconciliation step should validate
- **Solution**: Created modular agents that can be easily adjusted by domain experts

- **Challenge**: Getting agents to preserve original currencies without USD conversion
- **Solution**: Explicit prompting in tasks.yaml to maintain currency integrity

- **Challenge**: Avoiding hallucination in financial calculations
- **Solution**: Structured output formats and step-by-step validation requirements

### CrewAI Framework

I chose to use the CrewAI Framework because it supports multi-agent architecture, and provides clear separation of tasks and simple configuration. 

### Sequential Agents

**Attempted Hierarchical**: 
- Manager delegated widely → delegation sprawl
- Unpredictable execution paths → harder debugging
- Stalling on complex tasks

**Chose Sequential**:
- Predictable flow → easier testing
- Complete validation at each step → quality over speed
- Linear debugging → faster development

Given the short timeline, prioritizing simplicity and quality was crucial. In the future, I would spend time trying to develop a smart way to enable parallel execution where possible, which should reduce runtime.

### Why 8 Specialized Agents?

Instead of one "super agent" or few generalists:
- **Domain Expertise**: Each agent has deep knowledge in their specific area
- **Maintainability**: Modify one agent without affecting others
- **Auditability**: Clear responsibility chain 
- **Scalability**: Easy to add new agents

## Code Structure

```yaml
# agents.yaml - Define personas
tax_analyst:
  role: "Tax Rate Specialist"
  goal: "Identify treaty opportunities"
  backstory: "Expert in international tax..."

# tasks.yaml - Define workflows  
analyze_tax_rates:
  description: "Compare rates, find >1% differences..."
  agent: tax_analyst
```

```python
# crew.py - Orchestration
@CrewBase
class DividendReconciliationCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # Sequential execution with context passing
    process = Process.sequential
```

## Lessons Learned

1. **YAML Configuration is Powerful**: Business users can modify agent behavior without coding
2. **Context Preservation is Critical**: Each agent needs full context from previous agents
3. **Domain Knowledge Can Be Encoded**: Even without expertise, careful prompt engineering captures business logic
4. **LLMs Excel at Pattern Recognition**: The system caught data integrity issues (Nestle) that rules wouldn't detect
5. **Sequential Processing Has Trade-offs**: Slower but more reliable for financial data

## Future Enhancements

1. **Remediation Agents**: Auto-generate emails/Zwift tickets (using their API) to custodians
2. **Predictive Analytics**: Learn patterns from historical data
3. **Natural Language Interface**: "Show me all Samsung tax discrepancies"
4. **Hybrid Processing**: Parallel validators while maintaining sequential 
core
5. **Implement a Knowledge base**: Using a knowledge base that contains documentation on best practices for conducting a dividend reconciliation, historical break data + remediation steps etc. would be majorly helpful. A weakness to this application is that it lacks the context of how NBIM would solve a similar problem. Agentic Graph RAG!
