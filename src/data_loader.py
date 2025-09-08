"""
Simple data loader for dividend reconciliation
"""

import pandas as pd

def load_dividend_data(nbim_file: str, custody_file: str) -> str:
    """Load dividend data and create summary for AI analysis"""
    
    # Load CSV files
    nbim_df = pd.read_csv(nbim_file, sep=';')
    custody_df = pd.read_csv(custody_file, sep=';')
    
    summary = "DIVIDEND DATA COMPARISON:\n\n"
    
    for _, nbim_row in nbim_df.iterrows():
        event_key = str(nbim_row['COAC_EVENT_KEY'])
        company = nbim_row['ORGANISATION_NAME']
        
        # Find matching custody record
        custody_match = custody_df[custody_df['COAC_EVENT_KEY'].astype(str) == event_key]
        
        if len(custody_match) == 0:
            summary += f"{company}: No custody record found\n"
            continue
            
        custody_row = custody_match.iloc[0]
        
        # Extract amounts
        nbim_gross = float(nbim_row['GROSS_AMOUNT_QUOTATION'])
        nbim_net = float(nbim_row['NET_AMOUNT_QUOTATION'])
        nbim_tax = float(nbim_row['WTHTAX_COST_QUOTATION'])
        
        custody_gross = float(custody_row['GROSS_AMOUNT'])
        custody_net = float(custody_row['NET_AMOUNT_QC'])
        custody_tax = float(custody_row['TAX'])
        
        summary += f"""
{company}:
  NBIM:    Gross=${nbim_gross:,.0f}, Net=${nbim_net:,.0f}, Tax=${nbim_tax:,.0f}
  Custody: Gross=${custody_gross:,.0f}, Net=${custody_net:,.0f}, Tax=${custody_tax:,.0f}

"""
    
    return summary, len(nbim_df), len(custody_df)