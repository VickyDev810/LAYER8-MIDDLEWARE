from typing import Dict, List, Any

class PromptGenerator:
    """Generate effective prompts for anonymized queries based on LLM provider."""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize the prompt generator.
        
        Args:
            provider: The LLM provider ("openai", "anthropic", or "gemini")
        """
        self.provider = provider.lower()
        
        # Default system prompt template
        self.default_system_prompt = """
        You are a helpful assistant. You will receive a query that may contain placeholders for sensitive information in the format ___TYPE_ID___.
        
        Examples of placeholders:
        - ___PERSON_abc123___ (represents a person's name)
        - ___ORGANIZATION_def456___ (represents an organization name)
        - ___DATE_ghi789___ (represents a date)
        - ___PRODUCT_jkl012___ (represents a product name)
        
        Please respond naturally, keeping all placeholders in their original format without attempting to decode them.
        Do not refer to the placeholders as placeholders in your response, treat them as the actual entities they represent.
        """
        
        # Gemini-specific system prompt (since it handles prompts differently)
        self.gemini_system_prompt = """
        IMPORTANT INSTRUCTION: I will send you queries containing anonymized sensitive information with placeholders like ___TYPE_ID___.
        
        For example:
        - ___PERSON_abc123___ (a person's name)
        - ___ORGANIZATION_def456___ (an organization)
        - ___DATE_ghi789___ (a date)
        
        When you respond:
        1. Keep all placeholders in EXACTLY the same format
        2. Do not try to decode or guess the original values
        3. Treat the placeholders as if they are the actual entities they represent
        4. Do not mention that these are placeholders in your responses
        
        This is critical for privacy and security reasons.
        """
    
    def generate_system_prompt(self, sensitivity_report: Dict[str, List[str]]) -> str:
        """
        Generate a system prompt based on the sensitivity report and provider.
        
        Args:
            sensitivity_report: Dictionary of detected sensitive data categories
            
        Returns:
            A system prompt with context about detected placeholders
        """
        # Select appropriate base prompt for the provider
        if self.provider == "gemini":
            prompt = self.gemini_system_prompt
        else:
            prompt = self.default_system_prompt
        
        # Add detected entity types if available
        if sensitivity_report:
            prompt += "\n\nThis query contains the following types of sensitive data that have been anonymized:\n"
            for entity_type in sensitivity_report.keys():
                prompt += f"- {entity_type}\n"
                
        return prompt
    
    def generate_user_prompt(self, anonymized_query: str) -> str:
        """
        Generate the user prompt with the anonymized query.
        
        Args:
            anonymized_query: The query with sensitive data replaced by placeholders
            
        Returns:
            A user prompt with anonymized query and instructions
        """
        # Provider-specific user prompts
        if self.provider == "gemini":
            prompt = f"""
            Remember to maintain all placeholders (like ___TYPE_ID___) exactly as they appear.
            
            Query: {anonymized_query}
            """
        else:
            prompt = f"""
            Please respond to the following query. The query contains anonymized sensitive information
            represented by placeholders like ___TYPE_ID___. Please maintain these placeholders
            in exactly the same format in your response.
            
            Query: {anonymized_query}
            """
        return prompt.strip()