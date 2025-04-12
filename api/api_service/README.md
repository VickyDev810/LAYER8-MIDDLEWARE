# NLP Data Anonymizer API Service

A FastAPI-based service that provides secure anonymization of sensitive data for LLM interactions.

## 📋 Overview

This API service wraps the NLP Data Anonymizer functionality in a REST API, allowing you to:

1. **Anonymize** sensitive data in text (names, organizations, dates, etc.)
2. **Deanonymize** previously anonymized text
3. Process complete **queries** through the entire pipeline (anonymize → LLM → deanonymize)

## 🔧 Installation

1. Ensure you have the main project dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Install FastAPI-specific dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

3. Make sure your environment variables or `.env` file is set up with LLM API keys.

## 🚀 Running the API Server

Start the server with:

```bash
uvicorn api_service.main:app --reload
```

This will start the server at `http://localhost:8000` by default.

## 📚 API Endpoints

### 1. Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Check if the API is running and get basic info

### 2. Anonymize Text

#### A. Simple GET Method (for quick testing)
- **URL**: `/anonymize/{text}`
- **Method**: `GET`
- **Path Parameter**: 
  - `text`: The text to anonymize
- **Example**: `GET /anonymize/Jane%20Smith%20works%20at%20Acme%20Corp`

#### B. POST Method (for more complex data)
- **URL**: `/anonymize`
- **Method**: `POST`
- **Request Options**:
  - JSON Body:
    ```json
    {
      "text": "Your text with sensitive information"
    }
    ```
  - Query Parameter:
    - `text`: The text to anonymize
- **Response**:
  ```json
  {
    "anonymized_text": "Your text with ___PERSON_abc123___ placeholders",
    "sensitivity_report": {
      "person": ["John Doe"],
      "organization": ["Acme Corp"]
    },
    "formatted_report": "Sensitive Information Detected:\n- PERSON: John Doe\n- ORGANIZATION: Acme Corp"
  }
  ```

### 3. Deanonymize Text

#### A. Simple GET Method (for quick testing)
- **URL**: `/deanonymize/{text}`
- **Method**: `GET`
- **Path Parameter**: 
  - `text`: The anonymized text to restore
- **Example**: `GET /deanonymize/___PERSON_abc123___%20works%20at%20___ORGANIZATION_def456___`

#### B. POST Method (for more complex data)
- **URL**: `/deanonymize`
- **Method**: `POST`
- **Request Options**:
  - JSON Body:
    ```json
    {
      "text": "Text with ___PERSON_abc123___ placeholders"
    }
    ```
  - Query Parameter:
    - `text`: The anonymized text to restore
- **Response**:
  ```json
  {
    "original_text": "Text with original values restored"
  }
  ```

### 4. Process Query

#### A. Simple GET Method (for quick testing)
- **URL**: `/query/{query}`
- **Method**: `GET`
- **Path Parameter**: 
  - `query`: The query to process
- **Query Parameters (optional)**:
  - `provider`: LLM provider (gemini, openai, anthropic)
  - `model`: LLM model name
  - `temperature`: Temperature value (0.0-1.0)
  - `max_tokens`: Maximum tokens for response
- **Example**: `GET /query/Tell%20me%20about%20Project%20X?provider=gemini&temperature=0.8`

#### B. POST Method (for more complex data)
- **URL**: `/query`
- **Method**: `POST`
- **Request Options**:
  - JSON Body:
    ```json
    {
      "query": "Your query with sensitive information",
      "provider": "gemini",
      "model": "gemini-2.0-flash",
      "temperature": 0.7,
      "max_tokens": 1000
    }
    ```
  - Query Parameters:
    - `query`: The query to process
    - `provider`: LLM provider (optional)
    - `model`: LLM model name (optional)
    - `temperature`: Temperature value (optional)
    - `max_tokens`: Maximum tokens for response (optional)
- **Response**:
  ```json
  {
    "original_query": "Your original query",
    "anonymized_query": "Query with ___PERSON_abc123___ placeholders",
    "sensitivity_report": {
      "person": ["John Doe"],
      "organization": ["Acme Corp"]
    },
    "placeholder_mapping": {
      "person": [
        {
          "original_value": "John Doe",
          "placeholder": "___PERSON_abc123___"
        }
      ],
      "organization": [
        {
          "original_value": "Acme Corp",
          "placeholder": "___ORGANIZATION_def456___"
        }
      ]
    },
    "formatted_report": "Formatted sensitivity report",
    "llm_response": "LLM response with ___PERSON_abc123___ placeholders",
    "deanonymized_response": "LLM response with original values restored"
  }
  ```

## 📝 Client Example

The `client_example.py` script demonstrates how to use the API. Here are some examples:

```bash
# Process a query through the full pipeline
python -m api_service.client_example --query "Tell Jane Smith at Acme Corp about Project X"

# Anonymize text
python -m api_service.client_example --text "Jane Doe works at Acme Corp" --anonymize

# Deanonymize text
python -m api_service.client_example --text "___PERSON_abc123___ works at ___ORGANIZATION_def456___" --deanonymize

# Use a specific LLM provider
python -m api_service.client_example --query "Tell me about Project X" --provider openai
```

## ⚙️ Configuration

The service uses the main project's `config.json` file by default. You can also set configuration values using environment variables in a `.env` file:

```
HOST=0.0.0.0
PORT=8000
DEBUG=True
CONFIG_PATH=config.json
MAPPINGS_FILE=anonymizer_state.json
SPACY_MODEL=en_core_web_lg
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
DEFAULT_PROVIDER=gemini
```

## 🔒 Security Considerations

- In production, restrict CORS origins to trusted domains
- Implement proper authentication and rate limiting
- Ensure your API keys are kept secure
- Consider deploying behind a reverse proxy like Nginx 