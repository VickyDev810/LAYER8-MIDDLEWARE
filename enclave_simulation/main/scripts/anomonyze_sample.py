import re
import uuid

def anonymize(text: str):
    # Simple regex patterns for matching sensitive information
    patterns = {
        "credit_card": r"\b\d{4}-\d{4}-\d{4}-\d{4}\b|\b\d{16}\b",  # Credit card format (basic)
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Basic email pattern
    }
    
    # Function to generate unique placeholders
    def generate_placeholder(entity_type: str) -> str:
        return f"{entity_type}__{str(uuid.uuid4().int)[:8]}"
    
    # Replace sensitive data with placeholders
    for entity_type, pattern in patterns.items():
        text = re.sub(pattern, lambda match: generate_placeholder(entity_type), text)
    
    return text

# Example usage
x = input("Enter text with sensitive information: ")
anonymized_text = anonymize(x)
print("Anonymized text:", anonymized_text)
