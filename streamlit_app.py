"""
Simple Streamlit app for dividend reconciliation
"""

import streamlit as st
import sys
import os

# Add src to path
sys.path.append('src')

from data_loader import load_dividend_data
from reconciliation_crew import ReconciliationCrew

st.set_page_config(page_title="Simple CrewAI Prototype", layout="wide")

def main():
    st.title("Simple CrewAI Dividend Reconciliation")
    
    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_anthropic_api_key_here':
        st.error("Need Anthropic API key in .env file")
        return
    
    if st.button("Run CrewAI Analysis"):
        with st.spinner("Running simple analysis..."):
            run_crewai_analysis()

def run_crewai_analysis():
    """Simple CrewAI analysis using src modules"""
    
    try:
        # Load data using src module
        data_summary, nbim_count, custody_count = load_dividend_data(
            "data/NBIM_Dividend_Bookings 1.csv",
            "data/CUSTODY_Dividend_Bookings 1.csv"
        )
        
        st.success(f"Loaded {nbim_count} NBIM and {custody_count} custody records")
        
        # Run CrewAI analysis using src module
        crew = ReconciliationCrew()
        result = crew.analyze_dividends(data_summary)
        
        # Display result
        st.markdown("### CrewAI Analysis Result")
        st.write(result)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()