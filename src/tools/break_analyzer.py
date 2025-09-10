"""
Break Category Analysis Tool for Dividend Reconciliation
Detects specific business patterns that cause dividend discrepancies
"""

import pandas as pd
from typing import Type, Dict, List, ClassVar
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class BreakAnalysisInput(BaseModel):
    """Input for break analysis tool"""
    nbim_data: str = Field(..., description="NBIM data as text from Data Detective")
    custody_data: str = Field(..., description="Custody data as text from Data Detective")


class DividendBreakAnalyzer(BaseTool):
    """Intelligent break category detection for dividend reconciliation"""
    
    name: str = "dividend_break_analyzer"
    description: str = "Analyze dividend data to identify specific break categories and root causes"
    args_schema: Type[BaseModel] = BreakAnalysisInput

    # Break category definitions
    BREAK_CATEGORIES: ClassVar[Dict[str, Dict]] = {
        'LENDING_TAX_LEAKAGE': {
            'description': 'Tax penalty due to securities on loan during ex-date',
            'priority_threshold': 100000,  # $100k tax loss
            'resolution': 'Recall shares before ex-date or accept tax cost vs lending revenue'
        },
        
        'TREATY_MISAPPLICATION': {
            'description': 'Custodian not applying proper tax treaty rate',
            'priority_threshold': 50000,   # $50k reclaim opportunity
            'resolution': 'File reclaim with tax authorities or custodian error correction'
        },
        
        'FX_SPREAD_EXCESSIVE': {
            'description': 'Unfavorable FX rate applied by custodian',
            'priority_threshold': 0.01,    # 1% spread threshold
            'resolution': 'Negotiate better FX terms or switch execution venue'
        },
        
        'SETTLEMENT_DELAY': {
            'description': 'Payment received late affecting liquidity',
            'priority_threshold': 5,       # 5 days beyond standard
            'resolution': 'Escalate with custodian operations team'
        },
        
        'POSITION_MISMATCH': {
            'description': 'Share quantity differs between systems',
            'priority_threshold': 0,       # Any mismatch is critical
            'resolution': 'Verify corporate actions and investigate position breaks'
        }
    }

    def _run(self, nbim_data: str, custody_data: str) -> str:
        """Analyze data for break categories"""
        try:
            # Parse the data (simplified - in reality would parse structured data)
            analysis_results = []
            
            # Extract key information patterns
            nbim_lines = [line.strip() for line in nbim_data.split('\n') if line.strip()]
            custody_lines = [line.strip() for line in custody_data.split('\n') if line.strip()]
            
            # Pattern detection logic
            breaks_detected = self._detect_break_patterns(nbim_lines, custody_lines)
            
            for break_info in breaks_detected:
                category = break_info['category']
                event_key = break_info['event_key']
                details = break_info['details']
                priority = break_info['priority']
                
                analysis_results.append(
                    f"🔍 BREAK DETECTED: {category}\n"
                    f"   Event: {event_key}\n"
                    f"   Details: {details}\n"
                    f"   Priority: {priority}\n"
                    f"   Resolution: {self.BREAK_CATEGORIES[category]['resolution']}\n"
                )
            
            if not analysis_results:
                return "✅ NO SPECIFIC BREAK CATEGORIES DETECTED - Standard reconciliation analysis sufficient"
            
            result = "🔍 BREAK CATEGORY ANALYSIS:\n\n"
            result += "\n".join(analysis_results)
            result += f"\n\n📊 SUMMARY: {len(analysis_results)} specialized break patterns identified"
            
            return result
            
        except Exception as e:
            return f"Error in break analysis: {str(e)}"

    def _detect_break_patterns(self, nbim_lines: List[str], custody_lines: List[str]) -> List[Dict]:
        """Detect specific break patterns in the data"""
        detected_breaks = []
        
        # Extract event keys and related data
        events = self._extract_event_data(nbim_lines, custody_lines)
        
        for event_key, event_data in events.items():
            # Check for each break category
            
            # 1. LENDING TAX LEAKAGE
            if self._has_lending_tax_leakage(event_data):
                detected_breaks.append({
                    'category': 'LENDING_TAX_LEAKAGE',
                    'event_key': event_key,
                    'details': f"Securities on loan with higher tax rate: {event_data.get('tax_impact', 'N/A')}",
                    'priority': 'HIGH' if event_data.get('tax_loss', 0) > 100000 else 'MEDIUM'
                })
            
            # 2. TREATY MISAPPLICATION  
            if self._has_treaty_misapplication(event_data):
                detected_breaks.append({
                    'category': 'TREATY_MISAPPLICATION',
                    'event_key': event_key,
                    'details': f"Tax rate {event_data.get('applied_rate')} vs treaty rate {event_data.get('treaty_rate')}",
                    'priority': 'HIGH' if event_data.get('reclaim_amount', 0) > 50000 else 'MEDIUM'
                })
            
            # 3. FX SPREAD EXCESSIVE
            if self._has_excessive_fx_spread(event_data):
                detected_breaks.append({
                    'category': 'FX_SPREAD_EXCESSIVE',
                    'event_key': event_key,
                    'details': f"FX spread: {event_data.get('fx_spread_pct', 'N/A')}%",
                    'priority': 'MEDIUM'
                })
            
            # 4. SETTLEMENT DELAY
            if self._has_settlement_delay(event_data):
                detected_breaks.append({
                    'category': 'SETTLEMENT_DELAY',
                    'event_key': event_key,
                    'details': f"Payment delay: {event_data.get('delay_days', 'N/A')} days",
                    'priority': 'HIGH' if event_data.get('delay_days', 0) > 10 else 'MEDIUM'
                })
            
            # 5. POSITION MISMATCH
            if self._has_position_mismatch(event_data):
                detected_breaks.append({
                    'category': 'POSITION_MISMATCH',
                    'event_key': event_key,
                    'details': f"NBIM: {event_data.get('nbim_shares')} vs Custody: {event_data.get('custody_shares')}",
                    'priority': 'CRITICAL'
                })
        
        return detected_breaks

    def _extract_event_data(self, nbim_lines: List[str], custody_lines: List[str]) -> Dict:
        """Extract structured data from text lines"""
        events = {}
        
        # Simplified parsing - would be more sophisticated in production
        current_event = None
        
        for line in nbim_lines + custody_lines:
            if "COAC_EVENT_KEY:" in line:
                current_event = line.split(":")[-1].strip()
                if current_event not in events:
                    events[current_event] = {}
            elif current_event and any(field in line for field in ["Tax Rate", "Lending", "FX Rate", "Nominal Basis"]):
                # Extract relevant field data
                if "Tax Rate:" in line:
                    events[current_event]['applied_rate'] = line.split(":")[-1].strip()
                elif "Lending Percentage:" in line:
                    events[current_event]['lending_pct'] = line.split(":")[-1].strip()
                elif "FX Rate:" in line:
                    events[current_event]['fx_rate'] = line.split(":")[-1].strip()
                elif "Nominal Basis:" in line:
                    if 'nbim_shares' not in events[current_event]:
                        events[current_event]['nbim_shares'] = line.split(":")[-1].strip()
                    else:
                        events[current_event]['custody_shares'] = line.split(":")[-1].strip()
        
        return events

    def _has_lending_tax_leakage(self, event_data: Dict) -> bool:
        """Check for securities lending tax leakage"""
        # Simplified logic - would be more sophisticated in production
        lending_pct = event_data.get('lending_pct', '0').replace('%', '')
        try:
            return float(lending_pct) > 0
        except (ValueError, TypeError):
            return False

    def _has_treaty_misapplication(self, event_data: Dict) -> bool:
        """Check for tax treaty misapplication"""
        # Would compare applied rate vs expected treaty rate
        applied_rate = event_data.get('applied_rate', '0').replace('%', '')
        try:
            # Simplified: flag if rate > 20% (many treaties have lower rates)
            return float(applied_rate) > 20
        except (ValueError, TypeError):
            return False

    def _has_excessive_fx_spread(self, event_data: Dict) -> bool:
        """Check for excessive FX spread"""
        # Would compare custodian rate vs market mid-rate
        # Simplified implementation
        return 'fx_rate' in event_data  # Placeholder logic

    def _has_settlement_delay(self, event_data: Dict) -> bool:
        """Check for settlement delays"""
        # Would compare actual vs expected settlement dates
        # Simplified implementation  
        return False  # Placeholder logic

    def _has_position_mismatch(self, event_data: Dict) -> bool:
        """Check for position mismatches"""
        nbim_shares = event_data.get('nbim_shares', '0')
        custody_shares = event_data.get('custody_shares', '0')
        
        try:
            return float(nbim_shares) != float(custody_shares)
        except (ValueError, TypeError):
            return False