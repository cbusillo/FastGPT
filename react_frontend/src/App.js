import React, {useState} from 'react';
import {ThemeProvider, createTheme} from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import DarkModeToggle from './components/DarkModeToggle';
import FastGPTChat from './components/FastGPTChat';
import ModelSelector from './components/ModelSelector';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [selectedModel, setSelectedModel] = useState('');

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  const handleThemeChange = () => {
    setDarkMode(!darkMode);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline/>
      <Box sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%'
      }}>

        <ModelSelector selectedModel={selectedModel} setSelectedModel={setSelectedModel}/>
        <Box sx={{flex: 1, textAlign: 'center'}}>
          <Typography variant="h6">Welcome to FastGPT</Typography>
        </Box>
        <DarkModeToggle onChange={handleThemeChange} checked={darkMode}/>
      </Box>
      <FastGPTChat models={selectedModel}/>
    </ThemeProvider>
  );
}

export default App;
