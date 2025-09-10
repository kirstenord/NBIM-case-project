"""
Simplified Dividend Reconciliation Crew with 5 specialized agents
"""

import os
from crewai import Agent, Crew, Task, LLM, Process
from crewai.project import CrewBase, agent, crew, task, after_kickoff

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not available, skip loading
    pass


@CrewBase
class DividendReconciliationCrew():
    """Dividend reconciliation crew with 8 specialized agents"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    def __init__(self):
        # Initialize LLM with Anthropic Claude Sonnet 4 (latest and most powerful)
        self.llm = LLM(
            model="claude-sonnet-4-20250514",
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            temperature=0.3,  # Lower temperature for more consistent financial analysis
            max_tokens=8192  # Increased for detailed reconciliation reports
        )
    
    # 8 FOCUSED AGENTS
    @agent
    def data_detective(self) -> Agent:
        return Agent(
            config=self.agents_config['data_detective'],
            tools=[],  # No tools needed - data passed via inputs
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def math_calculator(self) -> Agent:
        return Agent(
            config=self.agents_config['math_calculator'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def position_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['position_validator'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def tax_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['tax_analyst'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def securities_lending_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['securities_lending_checker'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def fx_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['fx_validator'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def risk_prioritizer(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_prioritizer'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],
            llm=self.llm,
            verbose=True
        )
    
    # 8 FOCUSED TASKS
    @task
    def match_records_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_records'],
            agent=self.data_detective()
        )
    
    @task
    def calculate_differences_task(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_differences'],
            agent=self.math_calculator(),
            context=[self.match_records_task()]
        )
    
    @task
    def validate_positions_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_positions'],
            agent=self.position_validator(),
            context=[self.match_records_task()]
        )
    
    @task
    def analyze_tax_rates_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_tax_rates'],
            agent=self.tax_analyst(),
            context=[self.match_records_task()]
        )
    
    @task
    def check_securities_lending_task(self) -> Task:
        return Task(
            config=self.tasks_config['check_securities_lending'],
            agent=self.securities_lending_checker(),
            context=[self.match_records_task()]
        )
    
    @task
    def validate_fx_rates_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_fx_rates'],
            agent=self.fx_validator(),
            context=[self.match_records_task()]
        )
    
    @task
    def assess_risk_task(self) -> Task:
        return Task(
            config=self.tasks_config['assess_risk'],
            agent=self.risk_prioritizer(),
            context=[
                self.calculate_differences_task(),
                self.validate_positions_task(),
                self.analyze_tax_rates_task(),
                self.check_securities_lending_task(),
                self.validate_fx_rates_task()
            ]
        )
    
    @task
    def write_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_report'],
            agent=self.report_writer(),
            context=[
                self.match_records_task(),
                self.calculate_differences_task(),
                self.validate_positions_task(),
                self.analyze_tax_rates_task(),
                self.check_securities_lending_task(),
                self.validate_fx_rates_task(),
                self.assess_risk_task()
            ]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # type: ignore[attr-defined]
            tasks=self.tasks,    # type: ignore[attr-defined]
            process=Process.sequential,
            verbose=True
        )
    
    
    @after_kickoff  # type: ignore
    def process_output(self, output):
        """Process and enhance output after crew finishes"""
        
        # Add metadata to output
        from datetime import datetime
        processing_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Enhance the raw output with metadata
        enhanced_output = f"""
NBIM DIVIDEND RECONCILIATION REPORT
Generated: {processing_time}
System: 8-Agent Focused AI Reconciliation Crew

{output.raw}

---
SYSTEM METADATA:
- Agents Used: Data Matcher, Amount Calculator, Position Validator, Tax Analyst, Securities Lending Checker, FX Validator, Risk Prioritizer, Report Writer
- Processing Complete: {processing_time}
- Tools Used: SimpleRawCSV
- Model: claude-sonnet-4-20250514
"""
        
        output.raw = enhanced_output
        return output
    
    def run_reconciliation(self):
        """Run the reconciliation process with 8 focused agents"""
        
        # Read CSV files directly
        with open('data/NBIM_Dividend_Bookings 1.csv', 'r', encoding='utf-8-sig') as f:
            nbim_csv = f.read()
        
        with open('data/CUSTODY_Dividend_Bookings 1.csv', 'r', encoding='utf-8-sig') as f:
            custody_csv = f.read()
        
        # Pass CSV data directly to agents via kickoff inputs
        result = self.crew().kickoff(inputs={
            'nbim_csv_data': nbim_csv,
            'custody_csv_data': custody_csv
        })
        
        return result