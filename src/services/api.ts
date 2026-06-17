/**
 * API Service
 * Handles all communication with the Flask backend at http://192.168.4.139:5000/api
 */

// Type definitions for API responses
interface ChatResponse {
  response: string;
}

interface AgentsResponse {
  agents: string[];
}

const API_BASE_URL = 'http://192.168.4.139:5000/api';

/**
 * Check if the API backend is healthy and reachable
 * @returns Promise<boolean> - True if API is healthy, false otherwise
 */
export const checkAPIHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};

/**
 * Send a chat message to the backend and get AI response
 * @param message - The user's message to send to the AI
 * @returns Promise<string> - The AI's response
 * @throws Error if the request fails or the API returns an error
 */
export const sendChatMessage = async (message: string): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const data: ChatResponse = await response.json();
    return data.response;
  } catch (error) {
    console.error('Chat message failed:', error);
    throw new Error('Failed to send message. Please check your connection.');
  }
};

/**
 * Fetch available AI agents from the backend
 * @returns Promise<string[]> - Array of available agent names, empty array if request fails
 */
export const getAvailableAgents = async (): Promise<string[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/agents`);

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const data: AgentsResponse = await response.json();
    return data.agents;
  } catch (error) {
    console.error('Failed to fetch agents:', error);
    return [];
  }
};
