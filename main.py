#!/usr/bin/env python3
"""
Main Streamlit application for NBIM Dividend Reconciliation
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

from crews.crew import DividendReconciliationCrew

# Configure Streamlit page
st.set_page_config(
    page_title="NBIM Dividend Reconciliation", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """
    Main Streamlit application
    """
    # Title
    st.title("🏦 NBIM Dividend Reconciliation System")
    st.markdown("---")
    
    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("❌ ANTHROPIC_API_KEY not found in environment variables")
        st.info("Please add ANTHROPIC_API_KEY to your .env file")
        st.stop()
    
    # Check data files exist
    data_files = {
        "NBIM": "data/NBIM_Dividend_Bookings 1.csv",
        "Custody": "data/CUSTODY_Dividend_Bookings 1.csv"
    }
    
    missing_files = []
    for name, path in data_files.items():
        if not os.path.exists(path):
            missing_files.append(name)
    
    if missing_files:
        st.error(f"❌ Missing data files: {', '.join(missing_files)}")
        st.stop()
    
    # Simple interface with just the button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Run Reconciliation", type="primary", use_container_width=True, help="Start AI-powered dividend reconciliation"):
            run_reconciliation()
        
        # Instructions
        with st.expander("ℹ️ How it works"):
            st.markdown("""
            This system uses 8 specialized AI agents to reconcile dividend data:
            
            1. **Data Detective** - Parses and matches records
            2. **Math Calculator** - Calculates differences
            3. **Position Validator** - Validates share positions
            4. **Tax Analyst** - Analyzes tax rates
            5. **Securities Lending Checker** - Checks lending impact
            6. **FX Validator** - Validates FX rates
            7. **Risk Prioritizer** - Prioritizes issues
            8. **Report Writer** - Generates final report
            
            Click 'Run Reconciliation' to start the process.
            """)

def run_reconciliation():
    """Run the reconciliation and display results"""
    
    # Create placeholders for dynamic content
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    result_placeholder = st.empty()
    
    try:
        # Show progress
        with status_placeholder.container():
            st.info("🔄 Initializing AI agents...")
        
        progress_bar = progress_placeholder.progress(0)
        
        # Initialize crew
        crew = DividendReconciliationCrew()
        progress_bar.progress(20)
        
        with status_placeholder.container():
            st.info("🤖 Running multi-agent reconciliation...")
        
        # Run reconciliation
        start_time = datetime.now()
        result = crew.run_reconciliation()
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Clear progress indicators
        status_placeholder.empty()
        progress_placeholder.empty()
        
        # Success message
        st.success(f"✅ Reconciliation completed in {processing_time:.1f} seconds")
        
        # Display the report
        st.markdown("---")
        st.markdown("## 📊 Reconciliation Report")
        
        # Get the raw output as string
        if hasattr(result, 'raw'):
            report_text = result.raw
        else:
            report_text = str(result)
        
        # Display report in an expandable text area
        st.text_area(
            "Report Output",
            report_text,
            height=600,
            help="Full reconciliation report from AI agents"
        )
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download Report",
                data=report_text,
                file_name=f"reconciliation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download the full reconciliation report"
            )
        
        # Key findings section (if we can parse them)
        with st.expander("📌 View Key Findings"):
            if "EXECUTIVE SUMMARY" in report_text:
                # Try to extract executive summary
                try:
                    summary_start = report_text.find("EXECUTIVE SUMMARY")
                    summary_end = report_text.find("DETAILED FINDINGS", summary_start)
                    if summary_start != -1 and summary_end != -1:
                        summary = report_text[summary_start:summary_end]
                        st.text(summary)
                except:
                    st.text("Executive summary parsing failed. See full report above.")
            else:
                st.info("Executive summary not found in report. See full report above.")
        
    except Exception as e:
        # Clear any progress indicators
        status_placeholder.empty()
        progress_placeholder.empty()
        
        # Show error
        st.error(f"❌ Reconciliation failed: {str(e)}")
        with st.expander("🔍 Error Details"):
            st.exception(e)

if __name__ == "__main__":
    main()