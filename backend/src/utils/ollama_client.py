"""
Ollama Client - Connect to local LLM
Handles communication with Ollama running on http://192.168.4.139:11434
"""

import requests
import json
from typing import Optional

class OllamaClient:
    """
    Client to communicate with Ollama LLM service.
    
    Ollama runs locally and provides access to Mistral 7B model.
    Similar to how you'd use an API client in JavaScript.
    """
    
    def __init__(self, base_url: str = "http://192.168.4.139:11434"):
        """
        Initialize Ollama client.
        
        Parameters:
            base_url: URL where Ollama is running
        
        JavaScript equivalent:
        constructor(baseUrl = "http://192.168.4.139:11434") {
            this.baseUrl = baseUrl;
        }
        """
        self.base_url = base_url
        self.model = "mistral:latest"  # Our model name
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate response from LLM.
        
        Parameters:
            prompt: The question/instruction for the LLM
            stream: Whether to stream response (not used yet)
        
        Returns:
            str: The generated response from Mistral
        
        JavaScript equivalent:
        async generate(prompt, stream = false) {
            const response = await fetch(this.baseUrl + '/api/generate', {
                method: 'POST',
                body: JSON.stringify({
                    model: this.model,
                    prompt: prompt,
                    stream: false
                })
            });
            const data = await response.json();
            return data.response;
        }
        """
        try:
            # Build the API endpoint URL
            # Ollama's API endpoint for text generation
            url = f"{self.base_url}/api/generate"
            
            # Prepare request data
            payload = {
                "model": self.model,      # Use Mistral model
                "prompt": prompt,         # The user's prompt
                "stream": stream          # Don't stream (wait for full response)
            }
            
            # Make POST request to Ollama
            # Similar to: fetch(url, { method: 'POST', body: ... })
            response = requests.post(
                url,
                json=payload,             # Convert dict to JSON
                timeout=60               # Wait max 60 seconds
            )
            
            # Check if request was successful
            # 200 = success
            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.status_code}")
            
            # Parse the response JSON
            data = response.json()
            
            # Extract the generated text
            # data.response in JavaScript
            return data.get("response", "")
        
        except requests.exceptions.Timeout:
            # If it takes too long, raise error
            raise Exception("Ollama timeout - model might be slow")
        
        except requests.exceptions.ConnectionError:
            # If can't connect to Ollama
            raise Exception("Cannot connect to Ollama at " + self.base_url)
        
        except Exception as e:
            # Any other error
            raise Exception(f"Ollama error: {str(e)}")
    
    def is_healthy(self) -> bool:
        """
        Check if Ollama is running and healthy.
        
        Returns:
            bool: True if Ollama is available
        
        JavaScript equivalent:
        async isHealthy() {
            try {
                const response = await fetch(this.baseUrl + '/api/tags');
                return response.ok;
            } catch {
                return false;
            }
        }
        """
        try:
            # Try to fetch available models
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        
        except:
            # If any error, Ollama is not healthy
            return False
    
    def get_models(self) -> list:
        """
        Get list of available models in Ollama.
        
        Returns:
            list: List of model names
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                # Extract model names
                return [model["name"] for model in models]
            
            return []
        
        except:
            return []


# Create a singleton instance (one instance used everywhere)
# Like: export const ollama = new OllamaClient();
ollama = OllamaClient()