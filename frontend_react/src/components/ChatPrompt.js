//ChatPrompt.js
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import React, {useState} from "react";
import axios from 'axios';

const ChatPrompt = ({outputText, setOutputText, setOutputCodeText, selectedModel, testInput}) => {
  const [prompt, setPrompt] = useState('');
  const [conversationId, setConversationId] = useState(null); // Add state for conversation ID

  const startConversation = async () => {
    console.log('Starting conversation', selectedModel);
    const response = await axios.post('http://localhost:8000/conversations', {model_name: selectedModel});
    console.log('Conversation started', response.data);
    return response.data.conversation_id;
  };

  const getConversation = async () => {
    const response = await axios.get(`http://localhost:8000/conversations/${conversationId}`);
    setOutputText(response.data.messages.join('\n'));
  };

  const endConversation = async () => {
    await axios.delete(`http://localhost:8000/conversations/${conversationId}`);
    setConversationId(null);
  };

  const sendPrompt = async (currentPrompt) => {
    console.log('Sending prompt', selectedModel);
    let currentConversationId = conversationId;
    if (!currentConversationId) {
      currentConversationId = await startConversation();
    }
    await axios.post(`http://localhost:8000/conversations/${currentConversationId}/messages`, {
      model_name: selectedModel,
      message: currentPrompt,
      sender: 'User'
    });
    await getConversation();
    setPrompt('');
  };

  const handleKeydown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendPrompt(prompt);
    }
  };


  const clearConversation = async () => {
    if (conversationId) {
      await endConversation();
    }
    setOutputText('');
    setOutputCodeText('');
  };


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
        maxRows={10}
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
        <Button variant="contained">Test Code</Button>
      </Box>
    </Box>
  );
}

export default ChatPrompt;