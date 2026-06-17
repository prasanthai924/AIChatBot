"""
Flask API - Main backend server
Connects React frontend to AI agents.

Routes:
- GET  /api/health       - Check if API is working
- POST /api/chat         - Send message to AI
- GET  /api/agents       - List available agents
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from src.agents.chat_agent import ChatAgent
from src.agents.weather_agent import WeatherAgent
from src.agents.document_agent import DocumentAgent


# ============================================================
# Initialize Flask App
# ============================================================

app = Flask(__name__)

# Enable CORS (allow requests from React frontend on localhost:3000)
# Without this, React can't talk to Flask due to browser security
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ============================================================
# Initialize Agents
# ============================================================

# Create agent instances
chat_agent = ChatAgent()
weather_agent = WeatherAgent()
document_agent = DocumentAgent()

# Dictionary of all agents for easy access
agents = {
    "chat": chat_agent,
    "weather": weather_agent,
    "document": document_agent
}

print("✅ All agents initialized")
print(f"   - Chat Agent")
print(f"   - Weather Agent")
print(f"   - Document Agent")


# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================

@app.route("/api/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    
    React calls this to check if backend is running.
    
    Returns:
        JSON: {"status": "ok"}
    
    JavaScript equivalent:
    app.get("/api/health", (req, res) => {
        res.json({ status: "ok" });
    });
    """
    return jsonify({"status": "ok"})


# ============================================================
# LIST AGENTS ENDPOINT
# ============================================================

@app.route("/api/agents", methods=["GET"])
def list_agents():
    """
    Get list of available agents.
    
    Returns:
        JSON: {
            "agents": [
                {"name": "Chat Agent", "description": "..."},
                {"name": "Weather Agent", "description": "..."},
                ...
            ]
        }
    
    JavaScript equivalent:
    app.get("/api/agents", (req, res) => {
        const agents = Object.values(this.agents).map(a => a.getInfo());
        res.json({ agents });
    });
    """
    try:
        # Get info from each agent
        agents_info = [agent.get_info() for agent in agents.values()]
        
        return jsonify({
            "agents": agents_info,
            "count": len(agents_info)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# MAIN CHAT ENDPOINT
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.
    
    React sends user message here.
    We route to appropriate agent and return response.
    
    Request:
        POST /api/chat
        Body: {
            "message": "What's the weather in London?",
            "agent": "auto"  (optional, auto-detect if not provided)
        }
    
    Response:
        {
            "response": "The weather in London is...",
            "agent": "weather"
        }
    
    JavaScript equivalent:
    app.post("/api/chat", async (req, res) => {
        try {
            const { message, agent } = req.body;
            
            const selectedAgent = agent || this.detectAgent(message);
            const response = await agents[selectedAgent].process(message);
            
            res.json({ response, agent: selectedAgent });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get message from request
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Determine which agent to use
        # Either user specifies or we auto-detect
        agent_name = data.get("agent", "auto")
        
        if agent_name == "auto":
            agent_name = _detect_agent(user_message)
        
        # Check if agent exists
        if agent_name not in agents:
            return jsonify({
                "error": f"Agent '{agent_name}' not found",
                "available_agents": list(agents.keys())
            }), 400
        
        # Get the agent
        agent = agents[agent_name]
        
        # Process message
        print(f"📨 Message: {user_message}")
        print(f"🤖 Agent: {agent_name}")
        
        response = agent.process(user_message)
        
        print(f"💬 Response: {response[:100]}...")
        print()
        
        # Return response
        return jsonify({
            "response": response,
            "agent": agent_name,
            "agent_name": agent.name
        })
    
    except Exception as e:
        # Handle any errors
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


# ============================================================
# AGENT DETECTION
# ============================================================

def _detect_agent(message: str) -> str:
    """
    Auto-detect which agent to use based on message content.
    
    Logic:
    - If message has weather keywords → weather agent
    - If message asks about documents → document agent
    - Otherwise → chat agent
    
    Parameters:
        message: User's message
    
    Returns:
        str: Agent name ("weather", "document", or "chat")
    
    JavaScript equivalent:
    _detectAgent(message) {
        const lowerMsg = message.toLowerCase();
        
        if (lowerMsg.includes("weather") || lowerMsg.includes("temperature")) {
            return "weather";
        }
        
        if (lowerMsg.includes("document") || lowerMsg.includes("file")) {
            return "document";
        }
        
        return "chat";
    }
    """
    
    message_lower = message.lower()
    
    # Weather keywords
    weather_keywords = ["weather", "temperature", "rain", "snow", "wind", "humidity", "celsius", "fahrenheit", "forecast"]
    if any(keyword in message_lower for keyword in weather_keywords):
        return "weather"
    
    # Document keywords
    document_keywords = ["document", "file", "text", "know about", "tell me about", "what is", "define"]
    if any(keyword in message_lower for keyword in document_keywords):
        return "document"
    
    # Default to chat
    return "chat"


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI Chat Backend")
    print("=" * 60)
    print()
    print("📝 Agents initialized:")
    for name, agent in agents.items():
        print(f"   ✓ {agent.name}")
    print()
    print("🌐 Starting server...")
    print("   API: http://0.0.0.0:5000")
    print("   Frontend: http://localhost:3000")
    print()
    
    # Run Flask app
    # host='0.0.0.0' = accessible from network
    # port=5000 = the port
    # debug=True = auto-reload on code changes
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )