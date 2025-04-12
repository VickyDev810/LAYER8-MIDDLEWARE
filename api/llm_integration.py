import os
import json
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMIntegration:
    """Handle integration with LLM providers like OpenAI, Anthropic, and Google Gemini."""
    
    def __init__(self, provider: str = "openai", model: str = None):
        """
        Initialize the LLM integration.
        
        Args:
            provider: LLM provider ("openai", "anthropic", or "gemini")
            model: Model name to use (defaults to provider's recommended model)
        """
        self.provider = provider.lower()
        
        # Set default models if none provided
        if model is None:
            if self.provider == "openai":
                self.model = "gpt-4o"
            elif self.provider == "anthropic":
                self.model = "claude-3-sonnet-20240229"
            elif self.provider == "gemini":
                self.model = "gemini-2.0-flash"
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        else:
            self.model = model
        
        print(f"Model Name: {self.model}")  # Fixed print statement
            
        # Load API keys from environment variables
        if self.provider == "openai":
            self.api_key = os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
        elif self.provider == "anthropic":
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        elif self.provider == "gemini":
            self.api_key = os.environ.get("GOOGLE_API_KEY")
            if not self.api_key:
                # Try alternative environment variable name
                self.api_key = os.environ.get("GEMINI_API_KEY")
                if not self.api_key:
                    raise ValueError("Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set")
    
    def generate_response(self, 
                         prompt: str, 
                         system_message: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: int = 1000) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user message/query
            system_message: Optional system message for context
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in the response
            
        Returns:
            The LLM's response text
        """
        if self.provider == "openai":
            return self._call_openai(prompt, system_message, temperature, max_tokens)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt, system_message, temperature, max_tokens)
        elif self.provider == "gemini":
            return self._call_gemini(prompt, system_message, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai(self, 
                    prompt: str, 
                    system_message: Optional[str] = None,
                    temperature: float = 0.7,
                    max_tokens: int = 1000) -> str:
        """Call the OpenAI API and return the response."""
        try:
            import openai
            from openai import OpenAI
        except ImportError:
            raise ImportError("The 'openai' package is required for OpenAI integration. "
                             "Install it with 'pip install openai'")
        
        try:
            client = OpenAI(api_key=self.api_key)
            
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
    
    def _call_anthropic(self, 
                       prompt: str, 
                       system_message: Optional[str] = None,
                       temperature: float = 0.7,
                       max_tokens: int = 1000) -> str:
        """Call the Anthropic API and return the response."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("The 'anthropic' package is required for Anthropic integration. "
                             "Install it with 'pip install anthropic'")
        
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            
            system = system_message if system_message else "You are a helpful assistant."
            
            response = client.messages.create(
                model=self.model,
                system=system,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.content[0].text
        except Exception as e:
            return f"Error calling Anthropic API: {str(e)}"
        
    def _call_gemini(self, 
                    prompt: str, 
                    system_message: Optional[str] = None,
                    temperature: float = 0.7,
                    max_tokens: int = 1000) -> str:
        """Call the Google Gemini API and return the response."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("The 'google-generativeai' package is required for Gemini integration. "
                             "Install it with 'pip install google-generativeai'")
        
        try:
            # Configure the Google Generative AI library
            genai.configure(api_key=self.api_key)
            
            # Create a combined prompt for Gemini
            combined_prompt = prompt
            if system_message:
                combined_prompt = f"{system_message}\n\n{prompt}"
            
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 0
            }
            
            model = genai.GenerativeModel(model_name=self.model,
                                         generation_config=generation_config)
            response = model.generate_content(combined_prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"