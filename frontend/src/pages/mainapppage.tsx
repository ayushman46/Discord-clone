import { useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export default function MainAppPage() {
  // For now, we'll hardcode the channel ID to 1 for testing
  const channelId = 1;

  // Use our custom hook to manage the WebSocket connection
  const { messages, sendMessage } = useWebSocket(channelId);

  // State to manage the content of the message input box
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (newMessage.trim()) {
      sendMessage(newMessage);
      setNewMessage(''); // Clear the input box after sending
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Server List Column */}
      <div className="w-20 bg-gray-800 p-2">
        <p className="text-center font-bold">Servers</p>
      </div>

      {/* Channel List & User Info Column */}
      <div className="w-60 flex flex-col bg-gray-700">
        <div className="p-2 border-b border-gray-600">
          <h1 className="font-bold">Channel #{channelId}</h1>
        </div>
        <div className="flex-1 p-2">{/* Channel links will go here */}</div>
        <div className="p-2 border-t border-gray-600">
          <p>User Info</p>
        </div>
      </div>

      {/* Main Chat Area Column */}
      <div className="flex-1 flex flex-col bg-gray-600">
        <div className="p-2 border-b border-gray-500">
          <h2 className="font-bold">#general</h2>
        </div>
        {/* Message display area */}
        <div className="flex-1 p-4 space-y-2 overflow-y-auto">
          {messages.map((msg, index) => (
            <div key={index} className="bg-gray-700 p-2 rounded-md">
              {msg}
            </div>
          ))}
        </div>
        {/* Message input form */}
        <div className="p-4">
          <form onSubmit={handleSendMessage}>
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Message #general"
              className="w-full bg-gray-500 rounded p-2 focus:outline-none"
            />
          </form>
        </div>
      </div>
    </div>
  );
}