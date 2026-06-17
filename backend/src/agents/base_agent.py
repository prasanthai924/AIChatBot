"""
Base Agent - Abstract class for all agents
Defines the interface that all agents must implement.

Think of this like an interface in TypeScript:
interface IAgent {
    name: string;
    process(message: string): Promise<string>;
}
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.utils.ollama_client import ollama


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    
    All agents (ChatAgent, WeatherAgent, etc) inherit from this.
    They must implement the process() method.
    
    JavaScript equivalent:
    abstract class BaseAgent {
        abstract process(message: string): Promise<string>;
    }
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize agent.
        
        Parameters:
            name: Agent name (e.g., "Weather Agent")
            description: What this agent does
        
        JavaScript equivalent:
        constructor(name, description) {
            this.name = name;
            this.description = description;
        }
        """
        self.name = name
        self.description = description
        self.ollama = ollama  # Reference to LLM client
    
    @abstractmethod
    def process(self, message: str, **kwargs) -> str:
        """
        Process user message and return response.
        
        This method MUST be implemented by subclasses.
        If a subclass doesn't implement it, Python raises an error.
        
        Parameters:
            message: The user's input message
            **kwargs: Additional parameters specific to agent
        
        Returns:
            str: The agent's response
        
        JavaScript equivalent:
        abstract async process(message: string): Promise<string>;
        
        When you inherit from BaseAgent:
        class ChatAgent extends BaseAgent {
            async process(message) {
                // Must implement this!
            }
        }
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        Get agent information.
        
        Returns:
            Dictionary with name and description
        
        JavaScript equivalent:
        getInfo() {
            return {
                name: this.name,
                description: this.description
            };
        }
        """
        return {
            "name": self.name,
            "description": self.description
        }
    
    def _build_prompt(self, user_message: str, system_context: Optional[str] = None) -> str:
        """
        Build a formatted prompt for the LLM.
        
        This is a helper method (starting with _) used internally.
        
        Parameters:
            user_message: What the user asked
            system_context: Optional system instructions
        
        Returns:
            str: Formatted prompt for LLM
        
        JavaScript equivalent:
        _buildPrompt(userMessage, systemContext = null) {
            let prompt = "";
            if (systemContext) {
                prompt += systemContext + "\n\n";
            }
            prompt += "User: " + userMessage + "\n";
            prompt += "Assistant: ";
            return prompt;
        }
        """
        prompt = ""
        
        # Add system context if provided
        if system_context:
            prompt += f"{system_context}\n\n"
        
        # Add user message
        prompt += f"User: {user_message}\n"
        prompt += "Assistant: "
        
        return prompt
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate response using LLM.
        
        Helper method that calls Ollama to generate text.
        
        Parameters:
            prompt: The prompt to send to LLM
        
        Returns:
            str: Generated response
        
        JavaScript equivalent:
        async generateResponse(prompt) {
            try {
                const response = await this.ollama.generate(prompt);
                return response;
            } catch (error) {
                console.error("Error:", error);
                return "Error generating response";
            }
        }
        """
        try:
            # Call Ollama to generate response
            response = self.ollama.generate(prompt)
            return response.strip()  # Remove whitespace
        
        except Exception as e:
            # If error, return error message
            print(f"Error in {self.name}: {str(e)}")
            return f"Error: {str(e)}"


# Example of how subclasses will use this:
"""
class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__("Chat Agent", "Direct conversation with AI")
    
    def process(self, message: str, **kwargs) -> str:
        prompt = self._build_prompt(message)
        return self.generate_response(prompt)
"""