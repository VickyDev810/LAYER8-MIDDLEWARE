# Secure LLM Query System

A privacy-focused system that securely anonymizes sensitive data before sending queries to large language models (LLMs) like ChatGPT or Claude, and then de-anonymizes the responses.

## 📋 Overview

This system prevents the sharing of sensitive information with third-party LLM services while still getting useful responses. It uses NLP and pattern matching to detect and replace sensitive entities with placeholder tokens, sends anonymized queries to the LLM, and then restores the original entities in the response.

## 🔍 Key Features

- **Advanced Entity Detection**: Uses spaCy NLP models to identify named entities
- **Pattern Matching**: Detects emails, phone numbers, SSNs, and other sensitive patterns
- **Custom Term Detection**: Supports domain-specific sensitive terms
- **Persistence**: Save and load anonymization mappings
- **LLM Integration**: Works with OpenAI and Anthropic models
- **Interactive Mode**: Query LLMs securely from the command line

## 🗂️ Project Structure

```
.
├── main.py                          # Main entry point
├── config.json                      # Configuration file
├── llm_integration.py               # LLM API integration
├── prompt_generator.py              # System/user prompt generation
├── nlp_data_anonymizer/             # Core anonymization package
│   ├── __init__.py
│   ├── anonymizer.py                # Main anonymization orchestration
│   ├── entity_detection.py          # Named entity recognition
│   ├── pattern_matcher.py           # Regex-based pattern detection
│   ├── custom_term_detector.py      # Domain-specific term handling
│   └── persistence.py               # Save/load functionality
└── anonymizer_state.json            # Saved mappings state
```

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/secure-llm-query.git
   cd secure-llm-query
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install spaCy language model:
   ```bash
   python -m spacy download en_core_web_lg
   ```

5. Set API keys as environment variables:
   ```bash
   # For OpenAI
   export OPENAI_API_KEY=your_openai_api_key

   # For Anthropic (Claude)
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## 🚀 Usage

### Basic Usage

```python
from nlp_data_anonymizer import NLPDataAnonymizer
from llm_integration import LLMIntegration
from prompt_generator import PromptGenerator

# Initialize components
anonymizer = NLPDataAnonymizer()
llm = LLMIntegration(provider="openai", model="gpt-4o")
prompt_gen = PromptGenerator()

# Add domain-specific sensitive terms
anonymizer.add_domain_specific_terms("project", ["Project Alpha", "Operation Phoenix"])
anonymizer.add_domain_specific_terms("product", ["SecretProduct X9"])

# Process a query with sensitive information
query = "Please update Jane Smith about Project Alpha and the SecretProduct X9 launch."

# Analyze and anonymize the query
sensitivity_report = anonymizer.analyze_sensitivity(query)
anonymized_query = anonymizer.anonymize(query)

# Generate LLM prompts
system_prompt = prompt_gen.generate_system_prompt(sensitivity_report)
user_prompt = prompt_gen.generate_user_prompt(anonymized_query)

# Get response from LLM
response = llm.generate_response(prompt=user_prompt, system_message=system_prompt)

# De-anonymize the response
deanonymized_response = anonymizer.deanonymize(response)
```

### Command Line Interface

Run the system with sample query:
```bash
python main.py
```

Run in interactive mode:
```bash
python main.py --interactive
```

Use custom configuration:
```bash
python main.py --config custom_config.json
```

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "llm": {
    "provider": "openai",  // or "anthropic"
    "model": "gpt-4o",     // or other model names
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "anonymizer": {
    "model_name": "en_core_web_lg",
    "ner_confidence_threshold": 0.85,
    "save_mappings": true,
    "mappings_file": "anonymizer_state.json"
  },
  "domain_specific_terms": {
    "project": ["Project Alpha", "Operation Phoenix"],
    "product": ["SecretProduct X9"]
  }
}
```

## 🔒 Privacy Considerations

- All sensitive data remains local and is replaced with anonymous placeholders before sending to LLM APIs
- Placeholder tokens maintain the context while protecting the actual values
- Mappings between placeholders and sensitive data are stored locally
- No sensitive information is transmitted to third-party services

## 🧠 How It Works

1. **Detection**: Identifies sensitive entities using NLP models, regex patterns, and custom term lists
2. **Anonymization**: Replaces sensitive data with unique placeholder tokens
3. **Prompt Engineering**: Creates effective prompts instructing the LLM to maintain placeholders
4. **API Integration**: Sends anonymized queries to OpenAI or Anthropic APIs
5. **De-anonymization**: Restores original sensitive entities in the API response

## 📊 Example

**Original Query:**
```
I need a status update on Project Alpha for our CEO Jane Smith.
You can reach me at john.doe@company.com or (555) 123-4567.
```

**Anonymized Query:**
```
I need a status update on ___PROJECT_9982bfc7___ for our CEO ___PERSON_7ff71a51___.
You can reach me at ___EMAIL_d3fa2372___ or ___PHONE_58112389___.
```

**LLM Response (Anonymized):**
```
I'll prepare a status update on ___PROJECT_9982bfc7___ for ___PERSON_7ff71a51___.
Should I send it to ___EMAIL_d3fa2372___ or would you prefer I call ___PHONE_58112389___?
```

**De-anonymized Response:**
```
I'll prepare a status update on Project Alpha for Jane Smith.
Should I send it to john.doe@company.com or would you prefer I call (555) 123-4567?
```

## 🛠️ Extending the System

### Adding Custom Entity Types

```python
# In entity_detection.py
detector = EntityDetector()
detector.sensitive_entity_types["CUSTOM_TYPE"] = "custom_category"
```

### Adding New Pattern Matchers

```python
# In pattern_matcher.py
matcher = PatternMatcher()
matcher.add_pattern("credit_card", r'\b(?:\d{4}[- ]?){3}\d{4}\b')
```

### Supporting New LLM Providers

Extend the `LLMIntegration` class in `llm_integration.py` to support additional providers.

anonymizer.py: Core orchestration logic
entity_detection.py: NLP-based entity detection
pattern_matcher.py: Regex pattern matching
custom_term_detector.py: Custom term management
persistence.py: Saving/loading functionality

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.