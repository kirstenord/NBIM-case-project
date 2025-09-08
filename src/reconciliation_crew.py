"""
Simple CrewAI reconciliation engine
"""

import os
from crewai import Agent, Task, Crew, LLM

class ReconciliationCrew:
    """Simple crew for dividend reconciliation"""
    
    def __init__(self):
        self.llm = self._setup_llm()
    
    def _setup_llm(self) -> LLM:
        """Setup Claude LLM"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key == 'your_anthropic_api_key_here':
            raise ValueError("Need Anthropic API key in .env file")
            
        return LLM(
            model="claude-sonnet-4-20250514",
            api_key=api_key
        )
    
    def analyze_dividends(self, data_summary: str) -> str:
        """Run CrewAI analysis on dividend data"""
        
        # Create simple agent
        analyst = Agent(
            role="Dividend Reconciliation Analyst",
            goal="Compare dividend amounts and identify any differences",
            backstory="You compare numbers between two dividend files. Only report actual mathematical differences.",
            llm=self.llm,
            verbose=False
        )
        
        # Create analysis task
        task = Task(
            description=f"""
            Compare these dividend records and find actual differences:
            
            {data_summary}
            
            Rules:
            1. Only report differences > $1.00
            2. If amounts are identical, say "Perfect Match"  
            3. Be factual - no speculation
            4. Compare: Gross Amount, Net Amount, Tax Amount
            """,
            expected_output="List of companies with either 'Perfect Match' or actual dollar differences",
            agent=analyst
        )
        
        # Create and run crew
        crew = Crew(
            agents=[analyst],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        return str(result)