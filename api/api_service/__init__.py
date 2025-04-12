"""
NLP Data Anonymizer API Service

A FastAPI-based service that provides endpoints for:
- Anonymizing sensitive data in text
- Deanonymizing previously anonymized text
- Processing queries through the complete anonymize->LLM->deanonymize pipeline
"""

__version__ = "1.0.0" 