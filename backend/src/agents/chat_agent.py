"""
Chat Agent - Direct conversation with LLM
No tools, no context - just pure AI chat.

User: "What is artificial intelligence?"
Agent: Sends to Mistral → Gets response
"""

from src.agents.base_agent import BaseAgent


class ChatAgent(BaseAgent):
    """
    Simple chat agent for direct conversation with Mistral.
    
    Inherits from BaseAgent and implements the process() method.
    
    JavaScript equivalent:
    class ChatAgent extends BaseAgent {
        constructor() {
            super("Chat Agent", "...");
        }
        
        async process(message) {
            // Implementation
        }
    }
    """
    
    def __init__(self):
        """
        Initialize Chat Agent.
        
        Calls parent class constructor with name and description.
        """
        super().__init__(
            name="Chat Agent",
            description="Direct conversation with AI - ask anything!"
        )
        
        # System prompt - tells Mistral how to behave
        self.system_prompt = """You are a helpful AI assistant. 
Answer questions clearly and concisely. 
Be friendly and informative."""
    
    def process(self, message: str, **kwargs) -> str:
        """
        Process user message and return AI response.
        
        This is the main method called by the Flask API.
        
        Parameters:
            message: User's question/statement
            **kwargs: Unused (for compatibility with other agents)
        
        Returns:
            str: AI response
        
        Flow:
        1. Build prompt with system instructions
        2. Send to Ollama/Mistral
        3. Return response
        
        JavaScript equivalent:
        async process(message) {
            const prompt = this._buildPrompt(message, this.systemPrompt);
            const response = await this.generateResponse(prompt);
            return response;
        }
        """
        
        # Build the prompt
        # Includes system instructions + user message
        prompt = self._build_prompt(message, self.system_prompt)
        
        # Send to Ollama and get response
        response = self.generate_response(prompt)
        
        return response
    
    def process_with_context(self, message: str, conversation_history: list) -> str:
        """
        Process message with conversation history context.
        
        This allows the AI to remember previous messages in the chat.
        
        Parameters:
            message: Current user message
            conversation_history: List of previous messages
        
        Returns:
            str: AI response considering history
        
        Example:
        history = [
            {"role": "user", "text": "What is Python?"},
            {"role": "assistant", "text": "Python is..."},
        ]
        response = agent.process_with_context("Tell me more", history)
        
        JavaScript equivalent:
        async processWithContext(message, history) {
            let prompt = "";
            for (const msg of history) {
                prompt += `${msg.role}: ${msg.text}\n`;
            }
            prompt += `user: ${message}\nassistant: `;
            return await this.generateResponse(prompt);
        }
        """
        
        # Build prompt with conversation history
        prompt = self.system_prompt + "\n\n"
        
        # Add conversation history
        for msg in conversation_history:
            role = msg.get("role", "unknown")
            text = msg.get("text", "")
            # Capitalize first letter: user -> User
            prompt += f"{role.capitalize()}: {text}\n"
        
        # Add current message
        prompt += f"User: {message}\n"
        prompt += "Assistant: "
        
        # Generate response
        response = self.generate_response(prompt)
        
        return response


# Example usage:
if __name__ == "__main__":
    # Create agent
    agent = ChatAgent()
    
    # Test 1: Simple message
    print("Test 1: Simple message")
    response = agent.process("What is machine learning?")
    print(f"Response: {response}\n")
    
    # Test 2: With conversation history
    print("Test 2: With history")
    history = [
        {"role": "user", "text": "What is AI?"},
        {"role": "assistant", "text": "AI is artificial intelligence..."},
    ]
    response = agent.process_with_context("Tell me more about machine learning", history)
    print(f"Response: {response}")