import React, { useState } from 'react';
import { Send, Bot } from 'lucide-react';
import { useMutation } from 'react-query';
import { env } from '../env';
interface Message {
  role: 'user' | 'assistant'
  content: string
}

const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([
    { content: "Hello! I can help you explore the heatmap. Try asking about specific areas or data patterns.", role: 'assistant' }
  ]);

  const { mutate } = useMutation('chat', async () =>
    fetch(`${env.API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(messages)
    }).then(r => r.json()) as Promise<Message>
    , {
      onSettled: (data) => {
        if (!data) return
        console.log(data)
        setMessages(prev => [...prev, data]);
      }
    })

  const [input, setInput] = useState('');

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { content: input, role: 'user' };
    setMessages(prev => [...prev, userMessage]);

    setTimeout(mutate, 200)
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
            className={`flex ${message.role === 'assistant' ? 'justify-start' : 'justify-end'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${message.role === 'assistant'
                  ? 'bg-gray-100 text-gray-800'
                  : 'bg-indigo-600 text-white'
                }`}
            >
              {message.content}
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