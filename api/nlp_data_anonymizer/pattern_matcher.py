import re
from typing import List, Tuple, Dict


class PatternMatcher:
    def __init__(self):
        """
        Initialize the pattern matcher with regex patterns for sensitive data.
        """
        # Additional patterns for data that might be missed by NER
        self.additional_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b(?:\d{4}[- ]?){3}\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
    
    def detect_patterns(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Detect sensitive data using regex patterns.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of tuples (matched_text, pattern_type, start_pos, end_pos)
        """
        matches = []
        
        # Find regex pattern matches
        for pattern_type, pattern in self.additional_patterns.items():
            for match in re.finditer(pattern, text):
                matches.append((match.group(), pattern_type, match.start(), match.end()))
        
        return matches
        
    def add_pattern(self, pattern_type: str, pattern: str) -> None:
        """
        Add a new regex pattern for detection.
        
        Args:
            pattern_type: Category name for the pattern
            pattern: Regex pattern string
        """
        self.additional_patterns[pattern_type] = pattern