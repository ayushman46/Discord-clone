import { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import { api } from '@/lib/api';

interface Server {
  id: number;
  name: string;
  owner_id: number;
}

interface Channel {
  id: number;
  name: string;
  server_id: number;
}

export default function MainAppPage() {
  const [servers, setServers] = useState<Server[]>([]);
  const [selectedServer, setSelectedServer] = useState<Server | null>(null);
  const [channels, setChannels] = useState<Channel[]>([]);
  const [selectedChannel, setSelectedChannel] = useState<Channel | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const [newServerName, setNewServerName] = useState('');
  const [newChannelName, setNewChannelName] = useState('');
  const [showNewServerInput, setShowNewServerInput] = useState(false);
  const [showNewChannelInput, setShowNewChannelInput] = useState(false);
  const [isLoadingServers, setIsLoadingServers] = useState(true);
  const [uploadingFile, setUploadingFile] = useState(false);

  const channelId = selectedChannel?.id || 1;
  const { messages, typingUsers, isLoading, sendMessage, sendTypingIndicator } =
    useWebSocket(channelId);

  // Load servers on mount
  useEffect(() => {
    loadServers();
  }, []);

  // Load channels when server changes
  useEffect(() => {
    if (selectedServer) {
      loadChannels(selectedServer.id);
    }
  }, [selectedServer]);

  const loadServers = async () => {
    try {
      setIsLoadingServers(true);
      const data = await api.getUserServers();
      setServers(data || []);
      if (data && data.length > 0) {
        setSelectedServer(data[0]);
      }
    } catch (error) {
      console.error('Failed to load servers:', error);
    } finally {
      setIsLoadingServers(false);
    }
  };

  const loadChannels = async (serverId: number) => {
    try {
      const data = await api.getServerChannels(serverId);
      setChannels(data || []);
      if (data && data.length > 0) {
        setSelectedChannel(data[0]);
      }
    } catch (error) {
      console.error('Failed to load channels:', error);
    }
  };

  const handleCreateServer = async () => {
    if (!newServerName.trim()) return;
    try {
      const newServer = await api.createServer(newServerName);
      setServers([...servers, newServer]);
      setSelectedServer(newServer);
      setNewServerName('');
      setShowNewServerInput(false);
    } catch (error) {
      console.error('Failed to create server:', error);
    }
  };

  const handleCreateChannel = async () => {
    if (!newChannelName.trim() || !selectedServer) return;
    try {
      const newChannel = await api.createChannel(selectedServer.id, newChannelName);
      setChannels([...channels, newChannel]);
      setSelectedChannel(newChannel);
      setNewChannelName('');
      setShowNewChannelInput(false);
    } catch (error) {
      console.error('Failed to create channel:', error);
    }
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (newMessage.trim()) {
      sendMessage(newMessage);
      setNewMessage('');
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedChannel) return;

    try {
      setUploadingFile(true);
      const { file_url } = await api.uploadFile(selectedChannel.id, file);
      sendMessage(`[File uploaded: ${file.name}]`, file_url);
    } catch (error) {
      console.error('Failed to upload file:', error);
    } finally {
      setUploadingFile(false);
      e.target.value = '';
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewMessage(e.target.value);
    sendTypingIndicator();
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Server List Column */}
      <div className="w-20 bg-gray-800 p-2 flex flex-col items-center gap-2 overflow-y-auto">
        <p className="text-center font-bold text-xs py-2">Servers</p>
        {isLoadingServers ? (
          <p className="text-xs">Loading...</p>
        ) : (
          <>
            {servers.map((server) => (
              <button
                key={server.id}
                onClick={() => setSelectedServer(server)}
                className={`w-16 h-12 rounded-lg font-bold flex items-center justify-center transition ${
                  selectedServer?.id === server.id
                    ? 'bg-blue-600'
                    : 'bg-gray-700 hover:bg-gray-600'
                }`}
                title={server.name}
              >
                {server.name.substring(0, 2).toUpperCase()}
              </button>
            ))}
            <button
              onClick={() => setShowNewServerInput(!showNewServerInput)}
              className="w-16 h-12 rounded-lg bg-gray-700 hover:bg-gray-600 font-bold flex items-center justify-center transition"
              title="Create server"
            >
              +
            </button>
          </>
        )}
      </div>

      {/* Channel List & User Info Column */}
      <div className="w-60 flex flex-col bg-gray-700">
        {showNewServerInput && (
          <div className="p-2 border-b border-gray-600 bg-gray-800">
            <input
              type="text"
              value={newServerName}
              onChange={(e) => setNewServerName(e.target.value)}
              placeholder="Server name"
              className="w-full bg-gray-700 rounded p-2 text-white placeholder-gray-400 focus:outline-none mb-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleCreateServer();
              }}
            />
            <div className="flex gap-2">
              <button
                onClick={handleCreateServer}
                className="flex-1 bg-blue-600 hover:bg-blue-700 rounded p-1 text-sm"
              >
                Create
              </button>
              <button
                onClick={() => setShowNewServerInput(false)}
                className="flex-1 bg-gray-600 hover:bg-gray-500 rounded p-1 text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        <div className="p-2 border-b border-gray-600">
          <h1 className="font-bold text-lg">{selectedServer?.name || 'Select Server'}</h1>
        </div>

        {showNewChannelInput && selectedServer && (
          <div className="p-2 border-b border-gray-600 bg-gray-800">
            <input
              type="text"
              value={newChannelName}
              onChange={(e) => setNewChannelName(e.target.value)}
              placeholder="Channel name"
              className="w-full bg-gray-700 rounded p-2 text-white placeholder-gray-400 focus:outline-none mb-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleCreateChannel();
              }}
            />
            <div className="flex gap-2">
              <button
                onClick={handleCreateChannel}
                className="flex-1 bg-blue-600 hover:bg-blue-700 rounded p-1 text-sm"
              >
                Create
              </button>
              <button
                onClick={() => setShowNewChannelInput(false)}
                className="flex-1 bg-gray-600 hover:bg-gray-500 rounded p-1 text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        <div className="flex-1 p-2 overflow-y-auto">
          {channels.length > 0 ? (
            <>
              {channels.map((channel) => (
                <button
                  key={channel.id}
                  onClick={() => setSelectedChannel(channel)}
                  className={`w-full text-left px-3 py-2 rounded mb-1 transition ${
                    selectedChannel?.id === channel.id
                      ? 'bg-gray-600'
                      : 'hover:bg-gray-600'
                  }`}
                >
                  # {channel.name}
                </button>
              ))}
              {selectedServer && (
                <button
                  onClick={() => setShowNewChannelInput(!showNewChannelInput)}
                  className="w-full text-left px-3 py-2 rounded mt-2 bg-gray-800 hover:bg-gray-600 transition text-sm"
                >
                  + Add Channel
                </button>
              )}
            </>
          ) : (
            <p className="text-gray-400 text-sm">No channels yet</p>
          )}
        </div>

        <div className="p-2 border-t border-gray-600">
          <p className="text-sm">User Info</p>
        </div>
      </div>

      {/* Main Chat Area Column */}
      <div className="flex-1 flex flex-col bg-gray-600">
        <div className="p-2 border-b border-gray-500">
          <h2 className="font-bold text-lg">
            {selectedChannel ? `#${selectedChannel.name}` : '#general'}
          </h2>
        </div>

        {isLoading ? (
          <div className="flex-1 flex items-center justify-center">
            <p>Loading messages...</p>
          </div>
        ) : (
          <>
            <div className="flex-1 p-4 space-y-4 overflow-y-auto">
              {messages.map((msg, index) => (
                <div key={index} className="flex items-start">
                  <div className="flex flex-col">
                    <span
                      className={`font-bold text-sm ${
                        msg.type === 'user_joined' || msg.type === 'user_left'
                          ? 'text-yellow-400'
                          : 'text-white'
                      }`}
                    >
                      {msg.username}
                    </span>
                    <p className="text-gray-200">{msg.content}</p>
                    {msg.file_url && (
                      <a
                        href={msg.file_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-400 hover:text-blue-300 text-sm mt-1"
                      >
                        📎 View File
                      </a>
                    )}
                  </div>
                </div>
              ))}

              {typingUsers.size > 0 && (
                <div className="text-gray-400 italic text-sm">
                  {Array.from(typingUsers).join(', ')} is typing...
                </div>
              )}
            </div>

            <div className="p-4 border-t border-gray-500">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <input
                  type="file"
                  id="file-input"
                  onChange={handleFileUpload}
                  disabled={uploadingFile}
                  className="hidden"
                  accept="image/*,.pdf,.doc,.docx"
                />
                <button
                  type="button"
                  onClick={() => document.getElementById('file-input')?.click()}
                  disabled={uploadingFile}
                  className="bg-gray-500 hover:bg-gray-400 rounded p-2 transition disabled:opacity-50"
                  title="Upload file"
                >
                  📎
                </button>
                <input
                  type="text"
                  value={newMessage}
                  onChange={handleInputChange}
                  placeholder={selectedChannel ? `Message #${selectedChannel.name}` : 'Message #general'}
                  className="flex-1 bg-gray-500 rounded p-2 focus:outline-none"
                />
                <button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700 rounded px-4 py-2 transition"
                >
                  Send
                </button>
              </form>
            </div>
          </>
        )}
      </div>
    </div>
  );
}