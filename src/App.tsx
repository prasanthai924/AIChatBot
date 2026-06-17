/**
 * App Component
 * Root component that renders the ChatUI component
 */

import React from 'react';
import ChatUI from './components/ChatUI';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <ChatUI />
    </div>
  );
};

export default App;
