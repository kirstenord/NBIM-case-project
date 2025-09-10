"""
Simplest possible CSV tool - just returns raw data as lists of dictionaries
No processing, no aggregation - let the agents handle it
"""

import csv
import json
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class SimpleCSVInput(BaseModel):
    """Input for simple CSV tool"""
    load_both: bool = Field(True, description="Load both NBIM and Custody files")


class SimpleRawCSV(BaseTool):
    """Load CSV files and return raw data"""
    
    name: str = "load_raw_csv_data"
    description: str = "Load both NBIM and Custody CSV files and return raw unprocessed data as JSON lists"
    args_schema: Type[BaseModel] = SimpleCSVInput
    
    def _run(self, load_both: bool = True) -> str:
        """Load both files and return raw data"""
        
        try:
            # Read NBIM CSV
            nbim_data = []
            with open('data/NBIM_Dividend_Bookings 1.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                nbim_data = list(reader)
            
            # Read Custody CSV  
            custody_data = []
            with open('data/CUSTODY_Dividend_Bookings 1.csv', 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                custody_data = list(reader)
            
            # Return as simple JSON with basic metadata
            result = {
                "nbim_data": nbim_data,      # Raw list of dictionaries
                "custody_data": custody_data,  # Raw list of dictionaries
                "metadata": {
                    "nbim_rows": len(nbim_data),
                    "custody_rows": len(custody_data),
                    "nbim_fields": list(nbim_data[0].keys()) if nbim_data else [],
                    "custody_fields": list(custody_data[0].keys()) if custody_data else []
                }
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "message": "Failed to load CSV files"
            }
            return json.dumps(error_result, indent=2)