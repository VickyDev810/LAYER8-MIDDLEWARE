import requests
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Client for NLP Data Anonymizer API")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--query", help="Query to process")
    parser.add_argument("--text", help="Text to anonymize/deanonymize")
    parser.add_argument("--anonymize", action="store_true", help="Anonymize the text")
    parser.add_argument("--deanonymize", action="store_true", help="Deanonymize the text")
    parser.add_argument("--provider", default=None, help="LLM provider (openai, anthropic, gemini)")
    parser.add_argument("--model", default=None, help="LLM model name")
    parser.add_argument("--temperature", type=float, default=0.7, help="LLM temperature")
    args = parser.parse_args()
    
    base_url = args.url.rstrip("/")
    
    # Check if API is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return
            
        print(f"API Status: {response.json()['message']}")
        print(f"Default Provider: {response.json()['provider']}")
        print()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API at {base_url}")
        return
    
    # Process query using simplified endpoint
    if args.query:
        print(f"Processing query: {args.query}")
        
        # Build query parameters
        params = {}
        if args.provider:
            params["provider"] = args.provider
        if args.model:
            params["model"] = args.model
        if args.temperature:
            params["temperature"] = args.temperature
        
        # Use direct GET endpoint for better compatibility
        query_url = f"{base_url}/query/{requests.utils.quote(args.query)}"
        response = requests.get(query_url, params=params)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\nSensitivity Report:")
            print(result["formatted_report"])
            
            print("\nAnonymized Query:")
            print(result["anonymized_query"])
            
            # Show placeholders used in this query
            if "placeholder_mapping" in result:
                print("\nPlaceholder Mapping for Detected Entities:")
                for entity_type, entities in result["sensitivity_report"].items():
                    if not entities:
                        continue
                    print(f"\n{entity_type.upper()} placeholders:")
                    # Find placeholders for each detected entity
                    for entity in entities:
                        found = False
                        for mapping_type, mapping_items in result["placeholder_mapping"].items():
                            for item in mapping_items:
                                if item["original_value"] == entity:
                                    print(f"  {entity} → {item['placeholder']}")
                                    found = True
                                    break
                            if found:
                                break
                        if not found:
                            print(f"  {entity} → (No placeholder found)")
            
            print("\nLLM Response (Anonymized):")
            print(result["llm_response"])
            
            print("\nDeanonymized Response:")
            print(result["deanonymized_response"])
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    # Anonymize text using simplified endpoint
    elif args.text and args.anonymize:
        print(f"Anonymizing text: {args.text}")
        
        # Use direct GET endpoint for better compatibility
        anonymize_url = f"{base_url}/anonymize/{requests.utils.quote(args.text)}"
        response = requests.get(anonymize_url)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\nSensitivity Report:")
            print(result["formatted_report"])
            
            print("\nAnonymized Text:")
            print(result["anonymized_text"])
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    # Deanonymize text using simplified endpoint
    elif args.text and args.deanonymize:
        print(f"Deanonymizing text: {args.text}")
        
        # Use direct GET endpoint for better compatibility
        deanonymize_url = f"{base_url}/deanonymize/{requests.utils.quote(args.text)}"
        response = requests.get(deanonymize_url)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\nDeanonymized Text:")
            print(result["original_text"])
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    # No operation specified
    else:
        print("Please specify an operation: --query, --anonymize, or --deanonymize")
        print("Example: python client_example.py --query 'Tell me about Project X'")
        print("Example: python client_example.py --text 'Jane Doe works at Acme Corp' --anonymize")
        print("Example: python client_example.py --text '___PERSON_abc123___ works at ___ORGANIZATION_def456___' --deanonymize")

if __name__ == "__main__":
    main() 