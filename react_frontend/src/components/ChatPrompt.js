//ChatPrompt.js
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import React, {useCallback, useState} from "react";

const ChatPrompt = ({outputText, setOutputText, setOutputCodeText, websocketRef, connectWebsocket}) => {
  const [prompt, setPrompt] = useState('');

  const handleKeydown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendPrompt(prompt);
    }
  };


  const clearConversation = () => {
    setOutputText('');
    setOutputCodeText('');
  };

  const send = useCallback((currentPrompt) => {
    let userPrompt = outputText ? "\n\n" : "";
    userPrompt += `User: \n${currentPrompt}\n\nFastGPT: \n`;
    setOutputText(prev => prev + userPrompt);
    websocketRef.current.send(JSON.stringify({prompt: currentPrompt}));
    setPrompt('');
  }, [websocketRef, setOutputText, outputText]);

  const sendPrompt = useCallback((currentPrompt) => {
    if (!websocketRef.current ||
      websocketRef.current.readyState
      === WebSocket.CLOSED) {
      connectWebsocket();
    }
    if (websocketRef.current.readyState === WebSocket.CONNECTING) {
      websocketRef.current.addEventListener('open', () => {
        send(currentPrompt);
      }, {once: true});
    } else if (websocketRef.current.readyState === WebSocket.OPEN) {
      send(currentPrompt);
    }
  }, [websocketRef, connectWebsocket, send]);


  const sendTestPrompt = useCallback(() => {
    // noinspection LongLine
    sendPrompt("Write a Python script that generates a list of random integers between 1 and 100. The script should then calculate and print the mean, median, and standard deviation of these numbers. Use the 'random' module to generate the list and 'statistics' module for the calculations. Ensure to include necessary imports and handle any potential errors.");
  }, [sendPrompt]);

  return (
    <Box sx={{
      display: 'flex',
      paddingBottom: '1rem',
      paddingX: '1rem',
    }}>
      <TextField
        id="promptInput"
        label="Enter your prompt"
        multiline
        minRows={3}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        onKeyDown={handleKeydown}
        variant="outlined"
        sx={{
          flex: 1,
          mr: 1
        }}
      />
      <Box sx={{
        display: 'flex',
        flexDirection: 'column',
        ml: 1
      }}>
        <Button onClick={() => sendPrompt(prompt)} variant="contained" sx={{mb: 1}}>Generate</Button>
        <Button onClick={clearConversation} variant="outlined" sx={{mb: 1}}>Clear Conversation</Button>
        <Button onClick={sendTestPrompt} variant="contained">Test Code</Button>
      </Box>
    </Box>
  );
}

export default ChatPrompt;