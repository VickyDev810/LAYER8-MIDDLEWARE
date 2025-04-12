import json
import os
from typing import Dict
import datetime


class AnonymizerPersistence:
    """
    Handles saving and loading of anonymizer mappings and configuration.
    """
    
    @staticmethod
    def save_mappings(filename: str, anonymizer, create_new_file: bool = False) -> str:
        """
        Save the current anonymization mappings to a file.
        
        Args:
            filename: Path to save the mappings
            anonymizer: NLPDataAnonymizer instance
            create_new_file: If True, creates a new file with timestamp
            
        Returns:
            Path to the saved file
        """
        # Convert sets to lists for JSON serialization
        serializable_domain_terms = {
            k: list(v) for k, v in anonymizer.custom_detector.domain_specific_terms.items()
        }
        
        data = {
            "anonymized_map": anonymizer.anonymized_map,
            "custom_sensitive_terms": list(anonymizer.custom_detector.custom_sensitive_terms),
            "domain_specific_terms": serializable_domain_terms
        }
        
        # Create a new file with timestamp if requested
        if create_new_file:
            # Get filename without extension and add timestamp
            base_name = os.path.splitext(filename)[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{base_name}_{timestamp}.json"
            output_file = new_filename
        else:
            output_file = filename
            
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        return output_file
    
    @staticmethod
    def load_mappings(filename: str, anonymizer) -> None:
        """
        Load anonymization mappings from a file.
        
        Args:
            filename: Path to load the mappings from
            anonymizer: NLPDataAnonymizer instance
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            
        anonymizer.anonymized_map = data["anonymized_map"]
        anonymizer.custom_detector.custom_sensitive_terms = set(data["custom_sensitive_terms"])
        
        # Convert lists back to sets
        anonymizer.custom_detector.domain_specific_terms = {
            k: set(v) for k, v in data["domain_specific_terms"].items()
        }
        
        # Rebuild reverse map
        anonymizer.reverse_map = {v: k for k, v in anonymizer.anonymized_map.items()}
        
    @staticmethod
    def get_latest_mapping_file(base_filename: str) -> str:
        """
        Find the latest mapping file based on timestamp in filename.
        
        Args:
            base_filename: Base filename to search for
            
        Returns:
            Path to the latest mapping file, or the base filename if no timestamped files exist
        """
        base_name = os.path.splitext(base_filename)[0]
        directory = os.path.dirname(base_filename) or '.'
        
        # Find all files matching the pattern
        matching_files = []
        for file in os.listdir(directory):
            if file.startswith(base_name) and file.endswith('.json'):
                matching_files.append(os.path.join(directory, file))
                
        if not matching_files:
            return base_filename
            
        # Sort by modification time
        latest_file = max(matching_files, key=os.path.getmtime)
        return latest_file