//FastGPTChat.js
import React, {useCallback, useEffect, useRef, useState} from 'react';
import Box from '@mui/material/Box';

import ChatPrompt from './ChatPrompt';
import ChatOutput from './ChatOutput';


const FastGPTChat = () => {
  const [outputText, setOutputText] = useState('');
  const [outputCodeText, setOutputCodeText] = useState('');
  const outputContainerRef = useRef(null);
  const outputCodeContainerRef = useRef(null);
  const websocketRef = useRef(null);

  const connectWebsocket = useCallback(() => {
    if (websocketRef.current) {
      if (websocketRef.current.readyState === WebSocket.OPEN) {
        console.log('WebSocket is already open.');
        return;
      }
      if (websocketRef.current.readyState === WebSocket.CONNECTING) {
        console.log('WebSocket is already connecting.');
        return;
      }
    }
    console.log('Attempting to connect to WebSocket');
    websocketRef.current = new WebSocket('ws://localhost:8000/generate');

    websocketRef.current.onopen = () => {
      console.log('Connected to websocket');
    };

    websocketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.code) {
        setOutputCodeText(prev => prev + '\n\n' + data.code);
      } else if (data.response) {
        setOutputText(prev => prev + data.response);
      }
    };

    websocketRef.current.onclose = (event) => {
      console.log('Connection closed', event);
    };

    websocketRef.current.onerror = (event) => {
      console.log('Connection error', event);
      websocketRef.current.close();
    };
  }, []);

  useEffect(() => {
    connectWebsocket();
    return () => {
    };
  }, [connectWebsocket]);

  return (
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      height: '96vh'
    }}>
      <Box sx={{
        display: 'flex',
        flexGrow: 1,
        mb: 2,
        overflow: 'hidden'
      }}>
        <ChatOutput outputText={outputText} outputContainerRef={outputContainerRef}/>
        <ChatOutput outputText={outputCodeText} outputContainerRef={outputCodeContainerRef}/>
      </Box>
      <ChatPrompt outputText={outputText} setOutputText={setOutputText}
                  setOutputCodeText={setOutputCodeText}
                  websocketRef={websocketRef}
                  connectWebsocket={connectWebsocket}/>
    </Box>
  );
}

export default FastGPTChat;