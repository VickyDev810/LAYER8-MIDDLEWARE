import uuid
from typing import Dict, List, Set, Tuple, Any

from .entity_detection import EntityDetector
from .pattern_matcher import PatternMatcher
from .custom_term_detector import CustomTermDetector


class NLPDataAnonymizer:
    def __init__(self, model_name: str = "en_core_web_lg"):
        """
        Initialize the NLP-based data anonymizer.
        
        Args:
            model_name: Name of the spaCy model to use (requires installation)
        """
        # Initialize detection components
        self.entity_detector = EntityDetector(model_name)
        self.pattern_matcher = PatternMatcher()
        self.custom_detector = CustomTermDetector()
        
        # Initialize mapping dictionaries
        self.anonymized_map = {}
        self.reverse_map = {}
        
    def add_domain_specific_terms(self, category: str, terms: List[str]) -> None:
        """
        Add domain-specific terms that should be considered sensitive.
        
        Args:
            category: Category name for the terms
            terms: List of terms to anonymize
        """
        self.custom_detector.add_domain_specific_terms(category, terms)
    
    def train_on_data(self, sensitive_examples: List[str]) -> None:
        """
        Train the anonymizer by learning potential sensitive data from examples.
        
        Args:
            sensitive_examples: List of text examples containing sensitive data
        """
        for example in sensitive_examples:
            self.entity_detector.train_on_example(example, self.custom_detector)
    
    def _generate_placeholder(self, entity_type: str) -> str:
        """
        Generate a placeholder for anonymized data.
        
        Args:
            entity_type: Type of entity being anonymized
            
        Returns:
            A unique placeholder string
        """
        # Generate a short unique ID
        short_id = str(uuid.uuid4())[:8]
        return f"___{entity_type.upper()}_{short_id}___"
    
    def anonymize(self, text: str, reset_mappings: bool = False) -> str:
        """
        Anonymize sensitive data in the given text using NLP and pattern matching.
        
        Args:
            text: Input text containing sensitive information
            reset_mappings: If True, clear existing mappings before processing
            
        Returns:
            Anonymized text with sensitive data replaced
        """
        # Optionally reset mappings for new sessions
        if reset_mappings:
            self.anonymized_map = {}
            self.reverse_map = {}
            
        # Collect all potential sensitive data
        all_entities = []
        all_entities.extend(self.entity_detector.detect_entities(text))
        all_entities.extend(self.pattern_matcher.detect_patterns(text))
        all_entities.extend(self.custom_detector.detect_terms(text))
        
        # Sort entities by position (from end to start to avoid offset issues)
        all_entities.sort(key=lambda x: x[2], reverse=True)
        
        # Replace entities with placeholders
        anonymized_text = text
        for entity_text, entity_type, start_pos, end_pos in all_entities:
            # Skip very short entities (likely false positives)
            if len(entity_text) < 2:
                continue
                
            # Check if already anonymized
            if entity_text in self.reverse_map:
                placeholder = self.reverse_map[entity_text]
            else:
                placeholder = self._generate_placeholder(entity_type)
                self.anonymized_map[placeholder] = entity_text
                self.reverse_map[entity_text] = placeholder
            
            # Replace in text
            anonymized_text = anonymized_text[:start_pos] + placeholder + anonymized_text[end_pos:]
        
        return anonymized_text
    
    def deanonymize(self, text: str) -> str:
        """
        Restore anonymized data in the response text.
        
        Args:
            text: Text with anonymized placeholders
            
        Returns:
            Original text with sensitive data restored
        """
        for placeholder, original in self.anonymized_map.items():
            text = text.replace(placeholder, original)
        return text
    
    def analyze_sensitivity(self, text: str) -> Dict[str, List[str]]:
        """
        Analyze and classify sensitive data in text without anonymizing.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary mapping sensitivity categories to detected items
        """
        # Collect all potential sensitive data
        entities = self.entity_detector.detect_entities(text)
        entities.extend(self.pattern_matcher.detect_patterns(text))
        entities.extend(self.custom_detector.detect_terms(text))
        
        # Group by category
        sensitivity_report = {}
        for entity_text, entity_type, _, _ in entities:
            if entity_type not in sensitivity_report:
                sensitivity_report[entity_type] = []
            if entity_text not in sensitivity_report[entity_type]:
                sensitivity_report[entity_type].append(entity_text)
        
        return sensitivity_report
        
    def clear_mappings(self) -> None:
        """
        Clear all existing mappings.
        """
        self.anonymized_map = {}
        self.reverse_map = {}