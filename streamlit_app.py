"""
Enhanced Streamlit app for dividend reconciliation with 5-agent crew
"""

import streamlit as st
import sys
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

from crews.crew import DividendReconciliationCrew

st.set_page_config(
    page_title="NBIM Dividend Reconciliation System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🔍 NBIM Dividend Reconciliation System")
    st.markdown("### AI-Powered Multi-Agent Reconciliation")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Check API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            st.success("✅ API Key Configured")
        else:
            st.error("❌ Need ANTHROPIC_API_KEY in .env file")
            st.stop()
        
        st.markdown("---")
        st.markdown("### Agent Team")
        st.markdown("""
        1. 🔍 **Data Detective** - Matches records
        2. 🧮 **Math Calculator** - Calculates differences
        3. ⚠️ **Risk Assessor** - Prioritizes issues
        4. 🔎 **Investigation Helper** - Creates action plans
        5. 📊 **Report Writer** - Generates reports
        """)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Data Files")
        # Show data preview
        try:
            nbim_df = pd.read_csv('data/NBIM_Dividend_Bookings 1.csv', sep=';')
            custody_df = pd.read_csv('data/CUSTODY_Dividend_Bookings 1.csv', sep=';')
            
            st.metric("NBIM Records", len(nbim_df))
            st.metric("Custody Records", len(custody_df))
            
            # Show unique companies
            companies = nbim_df['ORGANISATION_NAME'].unique()
            st.markdown("**Companies:**")
            for company in companies:
                st.markdown(f"- {company}")
                
        except Exception as e:
            st.error(f"Error loading data files: {str(e)}")
    
    with col2:
        st.markdown("### Quick Stats")
        if 'nbim_df' in locals():
            # Calculate quick stats
            total_nbim_gross = nbim_df['GROSS_AMOUNT_QUOTATION'].sum()
            total_custody_gross = custody_df['GROSS_AMOUNT'].sum()
            
            st.metric("Total NBIM Gross", f"${total_nbim_gross:,.0f}")
            st.metric("Total Custody Gross", f"${total_custody_gross:,.0f}")
            st.metric("Gross Difference", f"${abs(total_nbim_gross - total_custody_gross):,.0f}")
    
    st.markdown("---")
    
    # Run reconciliation button
    if st.button("🚀 Run 5-Agent Reconciliation", type="primary", use_container_width=True):
        run_reconciliation()

def run_reconciliation():
    """Run the 5-agent reconciliation process"""
    
    # Create progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### Reconciliation Progress")
        
        # Create placeholders for each agent's status
        agent_status = {
            'detective': st.empty(),
            'calculator': st.empty(),
            'assessor': st.empty(),
            'investigator': st.empty(),
            'reporter': st.empty()
        }
        
        # Initialize statuses
        agent_status['detective'].info("🔍 Data Detective: Starting record matching...")
        agent_status['calculator'].info("🧮 Math Calculator: Waiting...")
        agent_status['assessor'].info("⚠️ Risk Assessor: Waiting...")
        agent_status['investigator'].info("🔎 Investigation Helper: Waiting...")
        agent_status['reporter'].info("📊 Report Writer: Waiting...")
    
    try:
        # Create and run the crew
        with st.spinner("Initializing AI crew..."):
            crew = DividendReconciliationCrew()
        
        # Update status as we go (in real implementation, this would be event-driven)
        agent_status['detective'].success("🔍 Data Detective: Matching complete!")
        agent_status['calculator'].info("🧮 Math Calculator: Calculating differences...")
        
        # Run the reconciliation
        with st.spinner("Running multi-agent reconciliation..."):
            result = crew.run_reconciliation()
        
        # Update all statuses to complete
        agent_status['detective'].success("🔍 Data Detective: Complete!")
        agent_status['calculator'].success("🧮 Math Calculator: Complete!")
        agent_status['assessor'].success("⚠️ Risk Assessor: Complete!")
        agent_status['investigator'].success("🔎 Investigation Helper: Complete!")
        agent_status['reporter'].success("📊 Report Writer: Complete!")
        
        # Display results
        st.markdown("---")
        st.markdown("## 📋 Reconciliation Results")
        
        # Create tabs for different sections of the report
        tab1, tab2, tab3 = st.tabs(["Executive Summary", "Detailed Findings", "Raw Output"])
        
        with tab1:
            st.markdown("### Executive Summary")
            # Parse and display executive summary from result
            st.info("""
            This section will contain:
            - Total events processed
            - Match rate percentage
            - High priority items requiring action
            - Estimated time saved
            """)
        
        with tab2:
            st.markdown("### Detailed Findings")
            # Parse and display detailed findings
            st.warning("""
            This section will contain:
            - Item-by-item breakdown
            - Specific discrepancy amounts
            - Recommended actions
            - Owner assignments
            """)
        
        with tab3:
            st.markdown("### Raw Agent Output")
            st.text(str(result))
        
        # Add export button
        st.download_button(
            label="📥 Download Full Report",
            data=str(result),
            file_name="reconciliation_report.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ Error during reconciliation: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()