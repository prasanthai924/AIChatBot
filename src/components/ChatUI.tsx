/**
 * ChatUI Component
 * Modern glassmorphism chat interface with agent detection and smooth animations
 * Displays animated agent indicators when specialized agents are triggered
 */

import React, { useState, useEffect, useRef } from 'react';
import { sendChatMessage, checkAPIHealth } from '../services/api';
import './ChatUI.css';

// Type definition for a chat message
interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: Date;
}

// Agent information
interface Agent {
  name: string;
  icon: string;
  color: string;
  description: string;
}

const AGENTS: Record<string, Agent> = {
  weather: {
    name: 'Weather Agent',
    icon: '🌍',
    color: '#0ea5e9',
    description: 'Fetching real-time weather data...'
  },
  chat: {
    name: 'Chat Agent',
    icon: '💬',
    color: '#8b5cf6',
    description: 'Thinking...'
  }
};

const ChatUI: React.FC = () => {
  // State management
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);
  const [activeAgent, setActiveAgent] = useState<Agent | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  /**
   * Effect: Check API health on mount and periodically
   * - Checks if the backend is running on first load
   * - Re-checks every 30 seconds to maintain connection status
   */
  useEffect(() => {
    const checkHealth = async () => {
      const isHealthy = await checkAPIHealth();
      setApiConnected(isHealthy);
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);

    return () => clearInterval(interval);
  }, []);

  /**
   * Effect: Auto-scroll to the bottom when new messages arrive
   * Provides smooth scrolling experience as conversation grows
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /**
   * Detect which agent should handle the request based on user message
   * @param message - User's message
   * @returns Agent object or null
   */
  const detectAgent = (message: string): Agent | null => {
    const lowerMessage = message.toLowerCase();

    // Check for weather-related keywords
    if (lowerMessage.includes('weather') ||
        lowerMessage.includes('temperature') ||
        lowerMessage.includes('rain') ||
        lowerMessage.includes('wind') ||
        lowerMessage.includes('forecast') ||
        (lowerMessage.includes('in ') && lowerMessage.includes('?'))) {
      return AGENTS.weather;
    }

    // Default to chat agent
    return AGENTS.chat;
  };

  /**
   * Handle form submission - validates input, sends message, and displays response
   * @param e - Form submission event
   */
  const handleSendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Skip if input is empty
    if (!inputValue.trim()) {
      return;
    }

    // Show alert if API is not connected
    if (!apiConnected) {
      alert('API is not connected. Please check your connection.');
      return;
    }

    // Store the message before clearing input
    const messageText = inputValue;

    // Create and display user message
    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: messageText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    // Detect and set active agent
    const agent = detectAgent(messageText);
    setActiveAgent(agent);
    setIsLoading(true);

    try {
      // Send message to backend and get AI response
      const aiResponse = await sendChatMessage(messageText);

      // Create and display AI response message
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: aiResponse,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      // Display error message if request fails
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setActiveAgent(null);
    }
  };

  /**
   * Format timestamp to HH:MM format
   * @param date - Date object to format
   * @returns Formatted time string
   */
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="chat-container">
      {/* Header Section */}
      <header className="chat-header">
        <div className="header-content">
          <h1>AI Chat</h1>
        </div>
        <div className={`connection-status ${apiConnected ? 'connected' : 'disconnected'}`}>
          <div className={`connection-indicator ${apiConnected ? 'connected' : 'disconnected'}`} />
          <span>{apiConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </header>

      {/* Connection Warning Banner */}
      {!apiConnected && (
        <div className="connection-warning">
          <span>Connection unavailable</span>
        </div>
      )}

      {/* Agent Indicator - shown when an agent is active */}
      {activeAgent && isLoading && (
        <div className="agent-indicator">
          <div className="agent-badge" style={{ borderColor: activeAgent.color }}>
            <span className="agent-icon">{activeAgent.icon}</span>
            <div className="agent-info">
              <div className="agent-name">{activeAgent.name}</div>
              <div className="agent-status">{activeAgent.description}</div>
            </div>
          </div>
        </div>
      )}

      {/* Messages Display Area */}
      <main className="messages-area">
        {/* Empty state - shown when no messages */}
        {messages.length === 0 && (
          <div className="empty-state">
            <h2>Start a conversation</h2>
            <p>Ask me anything or discuss any topic</p>
          </div>
        )}

        {/* Render all messages */}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message-group ${message.sender === 'user' ? 'user-group' : 'ai-group'}`}
          >
            <div className="message-bubble">
              <p>{message.text}</p>
            </div>
          </div>
        ))}

        {/* Loading indicator - shown while waiting for AI response */}
        {isLoading && (
          <div className="message-group ai-group">
            <div className="message-bubble loading">
              <div className="loading-animation">
                <div className="wave"></div>
                <div className="wave"></div>
                <div className="wave"></div>
              </div>
            </div>
          </div>
        )}

        {/* Invisible ref element used to scroll to bottom */}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Form Section */}
      <footer className="input-section">
        <form onSubmit={handleSendMessage} className="input-form">
          <div className="input-wrapper">
            <input
              type="text"
              className="message-input"
              placeholder="Message AI Chat..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isLoading || !apiConnected}
              autoFocus
            />
            <button
              type="submit"
              className="send-button"
              disabled={isLoading || !apiConnected || !inputValue.trim()}
              aria-label="Send message"
            >
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M10.5 1.5H3a1.5 1.5 0 0 0-1.5 1.5v12a1.5 1.5 0 0 0 1.5 1.5h14a1.5 1.5 0 0 0 1.5-1.5V9.5m-14-3h12m-4-3l3 3-3 3" />
              </svg>
            </button>
          </div>
          <p className="input-hint">
            {!apiConnected ? 'Connection unavailable' : 'Press Enter to send'}
          </p>
        </form>
      </footer>
    </div>
  );
};

export default ChatUI;
