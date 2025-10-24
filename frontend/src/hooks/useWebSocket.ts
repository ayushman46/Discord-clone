import { useEffect, useRef, useState, useCallback } from 'react';
import { useAuthStore } from '@/stores/authStore';

export interface ChatMessage {
  id?: number;
  username: string;
  content: string;
  timestamp: string;
  file_url?: string | null;
  type?: string;
}

const API_BASE_URL = (import.meta as any).env.VITE_API_URL || 'http://127.0.0.1:8000';

export function useWebSocket(channelId: number) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [typingUsers, setTypingUsers] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(true);
  const ws = useRef<WebSocket | null>(null);
  const token = useAuthStore((state) => state.token);
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Fetch message history
  const fetchMessageHistory = useCallback(async () => {
    if (!token) return;
    
    try {
      setIsLoading(true);
      const response = await fetch(`${API_BASE_URL}/channels/${channelId}/messages`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setMessages(data.map((msg: any) => ({
          id: msg.id,
          username: msg.owner.username,
          content: msg.content,
          timestamp: msg.timestamp || new Date().toISOString(),
          file_url: msg.file_url,
          type: 'message',
        })));
      }
    } catch (error) {
      console.error('Failed to fetch message history:', error);
    } finally {
      setIsLoading(false);
    }
  }, [channelId, token]);

  // Initialize WebSocket and fetch history on channel change
  useEffect(() => {
    if (!token) return;

    fetchMessageHistory();

    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${channelId}?token=${token}`);

    socket.onopen = () => {
      console.log(`WebSocket connected to channel ${channelId}`);
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        
        if (message.type === 'typing') {
          setTypingUsers((prev) => {
            const updated = new Set(prev);
            updated.add(message.username);
            return updated;
          });
          
          // Clear typing indicator after 3 seconds
          if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
          }
          typingTimeoutRef.current = setTimeout(() => {
            setTypingUsers((prev) => {
              const updated = new Set(prev);
              updated.delete(message.username);
              return updated;
            });
          }, 3000);
        } else if (message.type === 'message' || message.type === 'user_joined' || message.type === 'user_left') {
          setMessages((prevMessages) => [...prevMessages, message]);
        }
      } catch (error) {
        console.error('Failed to parse message:', error);
      }
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current = socket;

    return () => {
      socket.close();
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    };
  }, [channelId, token, fetchMessageHistory]);

  const sendMessage = useCallback((message: string, file_url?: string) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      const payload = {
        type: 'message',
        content: message,
        file_url: file_url || null,
      };
      ws.current.send(JSON.stringify(payload));
    }
  }, []);

  const sendTypingIndicator = useCallback(() => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      const payload = {
        type: 'typing',
      };
      ws.current.send(JSON.stringify(payload));
    }
  }, []);

  return { messages, typingUsers, isLoading, sendMessage, sendTypingIndicator };
}