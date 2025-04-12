import spacy
from typing import List, Tuple, Dict, Set


class EntityDetector:
    def __init__(self, model_name: str = "en_core_web_lg"):
        """
        Initialize the entity detector with a spaCy model.
        
        Args:
            model_name: Name of the spaCy model to use
        """
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model {model_name} not found. Please install it with:")
            print(f"python -m spacy download {model_name}")
            raise
            
        # Define entity categories for sensitive data
        self.sensitive_entity_types = {
            # Standard spaCy NER categories
            "PERSON": "person",
            "ORG": "organization",
            "GPE": "location",
            "LOC": "location",
            "DATE": "date",
            "TIME": "time",
            "MONEY": "financial",
            "PERCENT": "financial",
            "PHONE": "contact",
            "EMAIL": "contact",
            "URL": "contact",
            "PRODUCT": "product"
        }
        
        # Confidence threshold for NER
        self.ner_confidence_threshold = 0.85
        
    def detect_entities(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Detect sensitive entities using spaCy NER.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of tuples (entity_text, entity_type, start_pos, end_pos)
        """
        doc = self.nlp(text)
        entities = []
        
        # Get named entities from spaCy
        for ent in doc.ents:
            if ent.label_ in self.sensitive_entity_types:
                category = self.sensitive_entity_types[ent.label_]
                entities.append((ent.text, category, ent.start_char, ent.end_char))
        
        return entities
        
    def train_on_example(self, example: str, custom_detector) -> None:
        """
        Train on an example text to identify sensitive entities.
        
        Args:
            example: Example text containing sensitive data
            custom_detector: CustomTermDetector instance to update with new terms
        """
        doc = self.nlp(example)
            
        # Learn from named entities
        for ent in doc.ents:
            if ent.label_ in self.sensitive_entity_types and ent.text not in custom_detector.custom_sensitive_terms:
                custom_detector.add_single_term(ent.label_, ent.text)