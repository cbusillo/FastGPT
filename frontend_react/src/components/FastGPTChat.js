//FastGPTChat.js
import React, {useCallback, useEffect, useRef, useState} from 'react';
import Box from '@mui/material/Box';

import ChatPrompt from './ChatPrompt';
import ChatOutput from './ChatOutput';
import {API_CONFIG} from "../config";
import ModelSelector from "./ModelSelector";
import Typography from "@mui/material/Typography";
import Switch from "@mui/material/Switch";
import {FormControlLabel} from "@mui/material";


const FastGPTChat = () => {
  const [outputText, setOutputText] = useState('');
  const [outputCodeText, setOutputCodeText] = useState('');
  const outputContainerRef = useRef(null);
  const outputCodeContainerRef = useRef(null);
  const websocketRef = useRef(null);
  const [selectedModel, setSelectedModel] = useState('');
  const [testInput, setTestInput] = useState(false);

  function handleTestInputChange() {
    setTestInput(!testInput);
  }

  return (
    <Box sx={{display: 'flex', flexDirection: 'column', height: '96vh'}}>
      <Box sx={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: 1}}>
        <Typography variant="h6">Welcome to FastGPT 2.0</Typography>
        <FormControlLabel control={
          <Switch checked={testInput} onChange={handleTestInputChange} name="darkMode"/>
        }
                          label={"Test Input"}/>

        <ModelSelector selectedModel={selectedModel} setSelectedModel={setSelectedModel}/>
      </Box>
      <Box sx={{
        display: 'flex',
        flexGrow: 1,
        mb: 2,
        overflow: 'hidden'
      }}>
        <ChatOutput outputText={outputText} outputContainerRef={outputContainerRef}/>
        <ChatOutput outputText={outputCodeText} outputContainerRef={outputCodeContainerRef}/>
      </Box>
      <ChatPrompt
        outputText={outputText} setOutputText={setOutputText}
        setOutputCodeText={setOutputCodeText}
        websocketRef={websocketRef}
        selectedModel={selectedModel}
        testInput={testInput}
      />
    </Box>
  );
}

export default FastGPTChat;