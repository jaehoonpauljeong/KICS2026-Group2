'use client';

import { useState } from 'react';

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [input, setInput] = useState('');

    const handleSend = async () => {
    const text = input.trim();
    if (!text) return;

    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    setInput('');

    try {

      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ intent: text }),
      });

      if (!res.ok) {
        throw new Error('Request failed');
      }

      const data = await res.json();

      const explanation =
        `Got it. I translated your request into an I2NSF policy.\n` +
        `Intent: "${text}"\n\n` +
        `Here is the generated XML policy:\n\n` +
        (data.output ?? 'No output');

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: explanation },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Error: failed to generate policy.' },
      ]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex h-screen bg-white dark:bg-zinc-900">
      {/* Sidebar */}
      <div
        className={`bg-zinc-50 dark:bg-zinc-950 border-r border-zinc-200 dark:border-zinc-800 transition-all duration-200 ease-in-out overflow-hidden ${
          sidebarOpen ? 'w-64' : 'w-0 border-r-0'
        }`}
      >
        <div className="flex flex-col h-full p-4 w-64">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Menu</h2>
            <button
              onClick={() => setSidebarOpen(false)}
              className="p-1 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <button
            onClick={handleNewChat}
            className="flex items-center gap-3 px-4 py-3 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            <span className="text-sm font-medium">New Chat</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-col flex-1 min-w-0">
        {/* Header */}
        <header className="flex items-center gap-4 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          </button>
          <h1 className="text-lg font-medium text-zinc-800 dark:text-zinc-100">
            Security Policy Assistant
          </h1>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center max-w-md px-4">
                <h2 className="text-2xl font-semibold text-zinc-800 dark:text-zinc-100 mb-2">
                  Welcome to Security Policy Assistant
                </h2>
                <p className="text-zinc-600 dark:text-zinc-400">
                  Send high-level security intents and I&apos;ll translate them into low-level policies.
                </p>
              </div>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto py-8 px-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`mb-6 ${
                    message.role === 'user' ? 'flex justify-end' : 'flex justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-zinc-800 dark:bg-zinc-700 text-white'
                        : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-100'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-zinc-200 dark:border-zinc-800 p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex items-end gap-2">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Describe your security intent..."
                rows={1}
                className="flex-1 resize-none rounded-2xl border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 px-4 py-3 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:focus:ring-zinc-600 max-h-32"
                style={{ minHeight: '48px' }}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim()}
                className="flex items-center justify-center w-12 h-12 rounded-full bg-zinc-800 dark:bg-zinc-700 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-zinc-700 dark:hover:bg-zinc-600 transition-colors"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  stroke="currentColor"
                  className="w-5 h-5"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

