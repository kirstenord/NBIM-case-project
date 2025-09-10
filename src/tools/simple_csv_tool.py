"""
Simple CSV tool for reading dividend files with semicolon separators
"""

import pandas as pd
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from functools import lru_cache
import os
import time


class CSVInput(BaseModel):
    """Input for CSV tool"""
    file_path: str = Field(..., description="Path to CSV file")


class SimpleDividendCSV(BaseTool):
    """Simple tool to read dividend CSV files with semicolon separators"""
    
    name: str = "simple_dividend_csv"
    description: str = "Read dividend CSV files with semicolon separators and return the data"
    args_schema: Type[BaseModel] = CSVInput
    
    # Class-level cache to persist across tool instances
    _cache: Dict[str, tuple] = {}

    def _get_file_key(self, file_path: str) -> str:
        """Generate cache key based on file path and modification time"""
        try:
            stat = os.stat(file_path)
            return f"{file_path}_{stat.st_mtime}_{stat.st_size}"
        except:
            return file_path

    def _run(self, file_path: str) -> str:
        """Read CSV file and return comprehensive dynamic data with caching"""
        # Check cache first
        cache_key = self._get_file_key(file_path)
        if cache_key in self._cache:
            cached_result, timestamp = self._cache[cache_key]
            # Cache valid for 5 minutes
            if time.time() - timestamp < 300:
                return cached_result
        
        try:
            # Read CSV with semicolon separator
            df = pd.read_csv(file_path, sep=';')
            
            # Remove BOM if present
            if df.columns[0].startswith('\ufeff'):
                df.columns = [df.columns[0].replace('\ufeff', '')] + list(df.columns[1:])
            
            # Dynamic file type detection
            file_type = "NBIM" if 'GROSS_AMOUNT_QUOTATION' in df.columns else "Custody"
            
            # Format output with ALL fields dynamically
            result = f"Data from {file_path} ({file_type} format):\n"
            result += f"Records found: {len(df)}\n"
            result += f"Available fields ({len(df.columns)}): {', '.join(df.columns)}\n\n"
            
            # Show each record with ALL fields dynamically
            for idx, row in df.iterrows():
                result += f"Record {idx + 1}:\n"
                
                # Dynamically output all non-null fields
                for col in df.columns:
                    value = row.get(col, 'N/A')
                    if pd.notna(value) and str(value).strip() != '':
                        # Format field name for readability
                        formatted_field = col.replace('_', ' ').title()
                        result += f"  {formatted_field}: {value}\n"
                
                result += "\n"
            
            # Cache the result
            self._cache[cache_key] = (result, time.time())
            return result
            
        except Exception as e:
            error_msg = f"Error reading {file_path}: {str(e)}"
            return error_msg