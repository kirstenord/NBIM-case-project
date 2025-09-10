"""
Configuration for CrewAI built-in tools
Using existing CrewAI tools instead of creating custom ones
"""

from crewai_tools import CSVSearchTool, FileReadTool, DirectoryReadTool


def get_reconciliation_tools():
    """
    Initialize and return built-in CrewAI tools for reconciliation
    """
    
    # CSVSearchTool for searching within CSV files
    # This tool uses RAG for intelligent searching
    csv_search_nbim = CSVSearchTool(
        csv='data/NBIM_Dividend_Bookings 1.csv'
    )
    
    csv_search_custody = CSVSearchTool(
        csv='data/CUSTODY_Dividend_Bookings 1.csv'
    )
    
    # FileReadTool for reading entire files
    file_reader = FileReadTool()
    
    # DirectoryReadTool for reading all files in data directory
    directory_reader = DirectoryReadTool(
        directory='./data'
    )
    
    return {
        'csv_search_nbim': csv_search_nbim,
        'csv_search_custody': csv_search_custody,
        'file_reader': file_reader,
        'directory_reader': directory_reader
    }


def get_tool_descriptions():
    """
    Return descriptions of how each tool should be used
    """
    return {
        'csv_search_nbim': "Search for specific records in NBIM dividend bookings CSV file",
        'csv_search_custody': "Search for specific records in Custody dividend bookings CSV file", 
        'file_reader': "Read complete file contents when detailed analysis is needed",
        'directory_reader': "Read all files in the data directory for comprehensive analysis"
    }