import json
import os
import argparse
from typing import Dict, Any
from dotenv import load_dotenv

from nlp_data_anonymizer import NLPDataAnonymizer, AnonymizerPersistence
from llm_integration import LLMIntegration
from prompt_generator import PromptGenerator

# Load environment variables from .env file
load_dotenv()

def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """Load configuration from file."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def setup_anonymizer(config: Dict[str, Any]) -> NLPDataAnonymizer:
    """Set up the anonymizer with configuration."""
    anonymizer_config = config.get("anonymizer", {})
    model_name = anonymizer_config.get("model_name", "en_core_web_lg")
    
    anonymizer = NLPDataAnonymizer(model_name=model_name)
    
    # Add domain-specific terms if available
    domain_terms = config.get("domain_specific_terms", {})
    for category, terms in domain_terms.items():
        anonymizer.add_domain_specific_terms(category, terms)

    
    # Load existing mappings if available
    mappings_file = anonymizer_config.get("mappings_file", "anonymizer_state.json")
    if os.path.exists(mappings_file):
        AnonymizerPersistence.load_mappings(mappings_file, anonymizer)
        
    return anonymizer

def interactive_mode(anonymizer: NLPDataAnonymizer, llm_integration: LLMIntegration, 
                    prompt_generator: PromptGenerator, config: Dict[str, Any]):
    """Run the anonymizer in interactive mode."""
    print("=== Secure LLM Query System ===")
    print(f"Using {llm_integration.provider.upper()} ({llm_integration.model})")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("\nEnter your query: ")
        if query.lower() == 'exit':
            break
            
        print("\nProcessing query...")
        
        # Analyze and anonymize the query
        sensitivity_report = anonymizer.analyze_sensitivity(query)
        anonymized_query = anonymizer.anonymize(query)
        
        # Print sensitivity report
        print("\nSensitivity Analysis:")
        for category, items in sensitivity_report.items():
            print(f"  {category.upper()}: {', '.join(items)}")
            
        print("\nAnonymized Query:")
        print(anonymized_query)
        
        # Generate system and user prompts
        system_prompt = prompt_generator.generate_system_prompt(sensitivity_report)
        user_prompt = prompt_generator.generate_user_prompt(anonymized_query)
        
        print("\nSending to LLM...")
        
        # Generate response from LLM
        response = llm_integration.generate_response(
            prompt=user_prompt,
            system_message=system_prompt,
            temperature=config.get("llm", {}).get("temperature", 0.7),
            max_tokens=config.get("llm", {}).get("max_tokens", 1000)
        )
        
        print("\nAnonymized Response:")
        print(response)
        
        # Deanonymize the response
        deanonymized_response = anonymizer.deanonymize(response)
        
        print("\nDeanonymized Response:")
        print(deanonymized_response)
        
        # Save the current mappings
        if config.get("anonymizer", {}).get("save_mappings", True):
            AnonymizerPersistence.save_mappings(
                config.get("anonymizer", {}).get("mappings_file", "anonymizer_state.json"),
                anonymizer
            )

def main():
    parser = argparse.ArgumentParser(description="Secure LLM Query System")
    parser.add_argument("--config", default="config.json", help="Path to config file")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--provider", default=None, help="LLM provider: openai, anthropic, or gemini")
    parser.add_argument("--model", default=None, help="LLM model to use")
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line arguments if provided
    llm_config = config.get("llm", {})
    provider = args.provider or llm_config.get("provider", "gemini")
    model = args.model or llm_config.get("model")
    
    # Set up components
    anonymizer = setup_anonymizer(config)
    try:
        llm_integration = LLMIntegration(
            provider=provider,
            model=model
        )
        prompt_generator = PromptGenerator(provider=provider)
        
        if args.interactive:
            interactive_mode(anonymizer, llm_integration, prompt_generator, config)
        else:
            # Sample query example
            query = """
            I need a progress report on Project Horizon for our CTO, Emily Davis.
            We are evaluating potential risks from Zenith Technologies in the Asian market.
            Please include revenue forecasts for Q4 and specifics on the NovaX AI deployment.
            You can reach me at michael.lee@techfirm.com or (312) 987-6543.
            Additionally, we must address the data breach on December 5, 2023, at the London headquarters.
            I also want to propose Project Aegis, an initiative aimed at developing quantum-resistant cryptographic algorithms for our security infrastructure.
            """
            
            # Analyze and anonymize the query
            sensitivity_report = anonymizer.analyze_sensitivity(query)
            print("Sensitivity Analysis:")
            for category, items in sensitivity_report.items():
                print(f"  {category.upper()}: {', '.join(items)}")
            print("\n" + "-"*50 + "\n")
            
            anonymized_query = anonymizer.anonymize(query)
            print("Original Query:")
            print(query)
            print("\n" + "-"*50 + "\n")
            
            print("Anonymized Query:")
            print(anonymized_query)
            print("\n" + "-"*50 + "\n")
            
            # Generate system and user prompts
            system_prompt = prompt_generator.generate_system_prompt(sensitivity_report)
            user_prompt = prompt_generator.generate_user_prompt(anonymized_query)
            
            print("System Prompt:")
            print(system_prompt)
            print("\n" + "-"*50 + "\n")
            
            print("User Prompt:")
            print(user_prompt)
            print("\n" + "-"*50 + "\n")
            
            # Generate response from LLM if API keys are available
            try:
                response = llm_integration.generate_response(
                    prompt=user_prompt,
                    system_message=system_prompt,
                    temperature=llm_config.get("temperature", 0.7),
                    max_tokens=llm_config.get("max_tokens", 1000)
                )
                
                print("LLM Response (Anonymized):")
                print(response)
                print("\n" + "-"*50 + "\n")
                
                deanonymized_response = anonymizer.deanonymize(response)
                print("Deanonymized Response:")
                print(deanonymized_response)
                
                # Save mappings for later use
                AnonymizerPersistence.save_mappings("anonymizer_state.json", anonymizer)
            except Exception as e:
                print(f"Could not generate LLM response: {e}")
                print("Make sure your API key is correctly set in the .env file")
    except ValueError as e:
        print(f"Error initializing LLM: {e}")
        print("Make sure your API key is correctly set in the .env file")

if __name__ == "__main__":
    main()