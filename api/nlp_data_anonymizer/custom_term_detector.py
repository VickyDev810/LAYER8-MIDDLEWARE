from typing import List, Tuple, Dict, Set


class CustomTermDetector:
    def __init__(self):
        """
        Initialize the custom term detector for domain-specific terms.
        """
        self.custom_sensitive_terms = set()
        self.domain_specific_terms = {}
        
    def add_domain_specific_terms(self, category: str, terms: List[str]) -> None:
        """
        Add domain-specific terms that should be considered sensitive.
        
        Args:
            category: Category name for the terms
            terms: List of terms to anonymize
        """
        if category not in self.domain_specific_terms:
            self.domain_specific_terms[category] = set()
            
        self.domain_specific_terms[category].update(terms)
        self.custom_sensitive_terms.update(terms)
        
    def add_single_term(self, category: str, term: str) -> None:
        """
        Add a single term to the custom terms list.
        
        Args:
            category: Category name for the term
            term: Term to add
        """
        if category not in self.domain_specific_terms:
            self.domain_specific_terms[category] = set()
        
        self.domain_specific_terms[category].add(term)
        self.custom_sensitive_terms.add(term)
        
    def detect_terms(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Detect custom sensitive terms in the text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of tuples (term, category, start_pos, end_pos)
        """
        matches = []
        
        # Check for domain-specific terms
        for category, terms in self.domain_specific_terms.items():
            for term in terms:
                start = 0
                while True:
                    start = text.find(term, start)
                    if start == -1:
                        break
                    # Make sure we're matching whole words, not substrings
                    if (start == 0 or not text[start-1].isalnum()) and \
                       (start + len(term) == len(text) or not text[start + len(term)].isalnum()):
                        matches.append((term, category, start, start + len(term)))
                    start += 1
        
        return matches