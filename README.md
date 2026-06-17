# 🤖 AI Chat Application

A modern, full-stack chat application featuring real-time weather integration, LLM-powered responses, and a beautiful glassmorphism UI design.

**Live Demo:** [localhost:3000](http://localhost:3000)  
**Backend API:** [http://192.168.4.139:5000/api](http://192.168.4.139:5000/api)

---

## ✨ Features

### Frontend
- 🎨 **Glassmorphism Design** - Modern frosted glass UI with backdrop blur effects
- ✅ **Real-time Connection Status** - Live API health indicator with pulsing animation
- 🌍 **Weather Agent Integration** - Animated agent badge showing active agent
- ⚡ **Wave Loading Animation** - Smooth, modern loading indicator
- 📱 **Fully Responsive** - Mobile-first design that works on all devices
- 🎯 **Agent Auto-detection** - Automatically detects which agent to use based on message content
- 💬 **Message History** - Displays all messages with timestamps

### Backend
- 🔧 **Flask REST API** - Clean, modular API structure
- 🤖 **Multiple Agents** - Extensible agent system
  - **Chat Agent** - Direct LLM conversation
  - **Weather Agent** - Real weather data from OpenWeatherMap API
  - **Document Agent** - Document processing (extensible)
- 🧠 **Ollama Integration** - Local LLM (Mistral 7B) for response generation
- 🌍 **OpenWeatherMap API** - Real-time weather data for any location
- 🔐 **Environment Variables** - Secure configuration management
- 📝 **Comprehensive Logging** - Detailed request/response logging

### Security
- 🔒 **API Key Protection** - Secrets stored in `.env` files (never in code)
- 🚫 **Environment-based Configuration** - No hardcoded credentials
- ✅ **CORS Enabled** - Secure cross-origin requests
- 📚 **Security Documentation** - Complete security guidelines included

---

## 🏗️ Project Structure

```
react-chat-frontend/
├── 📁 backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── app.py                 # Flask application & API routes
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py      # Abstract base class for all agents
│   │   │   ├── chat_agent.py      # Direct LLM conversation agent
│   │   │   ├── weather_agent.py   # Real weather data agent
│   │   │   └── document_agent.py  # Document processing agent
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── ollama_client.py   # Ollama LLM client
│   ├── .env.example               # Backend environment template
│   ├── .env                        # Backend secrets (NOT in git)
│   ├── requirements.txt            # Python dependencies
│   └── venv/                       # Virtual environment
│
├── 📁 src/
│   ├── components/
│   │   ├── ChatUI.tsx             # Main chat component
│   │   └── ChatUI.css             # Chat styles (glassmorphism)
│   ├── services/
│   │   └── api.ts                 # API communication service
│   ├── App.tsx                    # Root component
│   ├── App.css                    # Global app styles
│   ├── index.tsx                  # React entry point
│   └── index.css                  # Global CSS reset
│
├── 📄 .env.example                # Frontend environment template
├── 📄 .gitignore                  # Git ignore rules
├── 📄 package.json                # npm dependencies
├── 📄 tsconfig.json               # TypeScript configuration
│
├── 📚 Documentation/
│   ├── SECURITY.md                # Security guidelines
│   ├── GIT_PUSH_SETUP.md          # Git setup guide
│   ├── README_DEPLOYMENT.md       # Deployment guide
│   └── GITIGNORE_GUIDE.md         # What to push/ignore
│
└── 📦 Dependencies/
    ├── node_modules/              # npm packages (NOT in git)
    ├── build/                     # React build output (NOT in git)
    └── backend/venv/              # Python venv (NOT in git)
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 14+ and npm 6+
- **Python** 3.8+
- **Ollama** running with Mistral model
- **OpenWeatherMap API Key** (free tier available)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/react-chat-frontend.git
cd react-chat-frontend
```

### 2️⃣ Setup Backend

```bash
# Navigate to backend
cd backend

# Create .env file
cp .env.example .env

# Edit .env with your API key
nano .env
# OPENWEATHER_API_KEY=your_actual_key_here
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Start Backend:**
```bash
python3 -m src.app
```

Backend runs on: `http://192.168.4.139:5000`

### 3️⃣ Setup Frontend

```bash
# Go back to root directory
cd ..

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: `http://localhost:3000`

---

## 📖 Usage

### Chat Interface

1. **Open** http://localhost:3000 in your browser
2. **Type** a message in the input field
3. **Send** by pressing Enter or clicking the Send button
4. **Watch** the animated loading indicator while AI responds

### Example Messages

#### 🌍 Weather Queries
```
"What’s the weather in London?"
"Tell me the temperature in New York"
"How’s the weather in Tokyo?"
"Is it raining in Paris?"
```

#### 💬 Chat Messages
```
"What is machine learning?"
"Explain quantum computing"
"Tell me about Python"
"What’s the difference between AI and ML?"
```

---

## 🔌 API Endpoints

### Health Check
```bash
GET /api/health

Response: { "status": "ok" }
```

### Send Message
```bash
POST /api/chat

Request:
{
  "message": "What’s the weather in London?",
  "agent": "auto"
}

Response:
{
  "response": "The weather in London is...",
  "agent": "weather",
  "agent_name": "Weather Agent"
}
```

### List Available Agents
```bash
GET /api/agents

Response:
{
  "agents": [
    { "name": "Chat Agent", "description": "..." },
    { "name": "Weather Agent", "description": "..." }
  ]
}
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend (`backend/.env`)
```env
OPENWEATHER_API_KEY=your_api_key_here
```

Get free API key at: https://openweathermap.org/api

#### Frontend (`.env.local` - optional)
```env
REACT_APP_API_URL=http://192.168.4.139:5000/api
```

### Required Services

**Ollama with Mistral:**
```bash
ollama serve
# In another terminal: ollama pull mistral:latest
```

**OpenWeatherMap API:**
- Sign up at https://openweathermap.org/api
- Create API key in Account → API keys
- Add to `backend/.env`

---

## 📊 Tech Stack

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- CSS3 - Glassmorphism styling
- Fetch API - HTTP client

### Backend
- Python 3.8+ - Programming language
- Flask - Web framework
- Flask-CORS - Cross-origin support
- Requests - HTTP client
- python-dotenv - Environment variables

### External APIs
- **Ollama** - Local LLM (Mistral 7B)
- **OpenWeatherMap** - Weather data

---

## 🧪 Testing

### Weather Agent
```bash
curl -X POST http://192.168.4.139:5000/api/chat \
  -H "Content-Type: application/json" \
  -d ‘{"message": "What is the weather in London?"}’
```

### Chat Agent
```bash
curl -X POST http://192.168.4.139:5000/api/chat \
  -H "Content-Type: application/json" \
  -d ‘{"message": "What is machine learning?"}’
```

### Health Check
```bash
curl http://192.168.4.139:5000/api/health
```

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running
ollama serve

# Verify with
curl http://192.168.4.139:11434/api/tags
```

### "API key is invalid" (401 error)
1. Go to https://openweathermap.org/api
2. Check your API key in Account → API keys
3. Ensure it’s activated
4. Update `backend/.env`

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Cannot connect to backend"
```bash
# Verify backend is running
curl http://192.168.4.139:5000/api/health

# Check frontend .env.local
cat .env.local
```

---

## 🔒 Security

✅ API keys stored in `.env` files  
✅ `.env` excluded from git  
✅ `.env.example` provides templates  
❌ Never commit actual `.env` files  

See [`SECURITY.md`](./SECURITY.md) for detailed guidelines.

---

## 📚 Documentation

- [`SECURITY.md`](./SECURITY.md) - Security guidelines
- [`GIT_PUSH_SETUP.md`](./GIT_PUSH_SETUP.md) - Git instructions
- [`README_DEPLOYMENT.md`](./README_DEPLOYMENT.md) - Deployment guide
- [`GITIGNORE_GUIDE.md`](./GITIGNORE_GUIDE.md) - What to push/ignore

---

## 🚀 Production Build

```bash
npm run build
# Creates optimized build in /build directory
```

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m ‘Add amazing feature’`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<div align="center">

Made with ❤️ using React, Flask, and Claude AI

[⭐ Star this repo](https://github.com/YOUR_USERNAME/react-chat-frontend) if you find it helpful!

</div>
