import os
import json
import sys
from typing import Dict, Any, List, Tuple

# Add parent directory to path if needed for direct script execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from nlp_data_anonymizer import NLPDataAnonymizer, AnonymizerPersistence

# Import local modules
try:
    # When running as a module
    from api_service.config import settings
except ImportError:
    # When running with relative imports
    from .config import settings

def load_json_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from JSON file with fallbacks.
    
    Args:
        config_path: Path to the config file
        
    Returns:
        Dictionary with configuration values
    """
    path = config_path or settings.CONFIG_PATH
    
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config file {path}: {e}")
    
    # Default configuration if file doesn't exist or is invalid
    return {
        "llm": {
            "provider": settings.DEFAULT_PROVIDER,
            "model": settings.DEFAULT_MODEL,
            "temperature": settings.DEFAULT_TEMPERATURE,
            "max_tokens": settings.DEFAULT_MAX_TOKENS
        },
        "anonymizer": {
            "model_name": settings.SPACY_MODEL,
            "ner_confidence_threshold": 0.85,
            "save_mappings": True,
            "mappings_file": settings.MAPPINGS_FILE
        },
        "domain_specific_terms": {}
    }

def save_anonymizer_state(anonymizer: NLPDataAnonymizer, mappings_file: str = None) -> bool:
    """
    Save the current state of the anonymizer.
    
    Args:
        anonymizer: The anonymizer instance
        mappings_file: Path to save the mappings
        
    Returns:
        True if successful, False otherwise
    """
    path = mappings_file or settings.MAPPINGS_FILE
    
    try:
        AnonymizerPersistence.save_mappings(path, anonymizer)
        return True
    except Exception as e:
        print(f"Error saving anonymizer state: {e}")
        return False

def load_anonymizer_state(anonymizer: NLPDataAnonymizer, mappings_file: str = None) -> bool:
    """
    Load the state of the anonymizer.
    
    Args:
        anonymizer: The anonymizer instance
        mappings_file: Path to load the mappings from
        
    Returns:
        True if successful, False otherwise
    """
    path = mappings_file or settings.MAPPINGS_FILE
    
    if os.path.exists(path):
        try:
            AnonymizerPersistence.load_mappings(path, anonymizer)
            return True
        except Exception as e:
            print(f"Error loading anonymizer state: {e}")
    
    return False

def format_sensitivity_report(sensitivity_report: Dict[str, List[str]]) -> str:
    """
    Format the sensitivity report for human-readable output.
    
    Args:
        sensitivity_report: Dictionary of detected sensitive data
        
    Returns:
        Formatted string report
    """
    if not sensitivity_report:
        return "No sensitive information detected."
    
    report = "Sensitive Information Detected:\n"
    for category, items in sensitivity_report.items():
        report += f"\n- {category.upper()}: {', '.join(items)}"
    
    return report

def get_placeholder_mapping(anonymizer: NLPDataAnonymizer) -> Dict[str, List[Tuple[str, str]]]:
    """
    Generate a mapping dictionary that relates original values to placeholders, grouped by category.
    
    Args:
        anonymizer: The anonymizer instance with populated mappings
        
    Returns:
        Dictionary mapping categories to lists of (original_value, placeholder) tuples
    """
    # Create reverse mapping from placeholder to original values
    placeholder_to_original = {v: k for k, v in anonymizer.reverse_map.items()}
    
    # Group by category (extracted from placeholder pattern ___CATEGORY_id___)
    mapping_by_category = {}
    
    for placeholder, original in placeholder_to_original.items():
        try:
            # Extract category from placeholder (___CATEGORY_id___)
            parts = placeholder.strip('_').split('_')
            if len(parts) >= 2:
                category = parts[0].lower()
                
                if category not in mapping_by_category:
                    mapping_by_category[category] = []
                    
                mapping_by_category[category].append({
                    "original_value": original,
                    "placeholder": placeholder
                })
        except Exception:
            # Skip any placeholders that don't match the expected format
            continue
            
    return mapping_by_category 