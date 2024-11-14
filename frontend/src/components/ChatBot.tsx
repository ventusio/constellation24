import React, { useState } from 'react';
import { Send, Bot } from 'lucide-react';

interface Message {
  text: string;
  isBot: boolean;
}

const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I can help you explore the heatmap. Try asking about specific areas or data patterns.", isBot: true }
  ]);
  const [input, setInput] = useState('');

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { text: input, isBot: false };
    setMessages(prev => [...prev, userMessage]);

    // Simulate bot response
    setTimeout(() => {
      const botResponse = { 
        text: "I see you're interested in the map. I can help you analyze patterns and explore different areas.", 
        isBot: true 
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);

    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <div className="p-4 border-b bg-indigo-600 rounded-t-lg">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <Bot className="w-6 h-6" />
          Map Assistant
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${
                message.isBot
                  ? 'bg-gray-100 text-gray-800'
                  : 'bg-indigo-600 text-white'
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about the heatmap..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            type="submit"
            className="p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatBot;