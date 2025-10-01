import { useEffect, useRef, useState } from 'react';

export function useWebSocket(channelId: number) {
  // State to hold the array of messages
  const [messages, setMessages] = useState<string[]>([]);

  // Use a ref to hold the WebSocket instance, which persists across renders
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Create a new WebSocket connection when the component mounts or channelId changes
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${channelId}`);

    // Event listener for when the connection is opened
    socket.onopen = () => {
      console.log(`WebSocket connected to channel ${channelId}`);
    };

    // Event listener for receiving messages from the server
    socket.onmessage = (event) => {
      // Add the new message to our messages array
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    // Event listener for when the connection closes
    socket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    // Store the WebSocket instance in our ref
    ws.current = socket;

    // Cleanup function: This will run when the component unmounts
    return () => {
      socket.close();
    };
  }, [channelId]); // The effect re-runs if the channelId changes

  // A function to send a message through the WebSocket
  const sendMessage = (message: string) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message);
    }
  };

  // Return the messages and the sendMessage function for the component to use
  return { messages, sendMessage };
}