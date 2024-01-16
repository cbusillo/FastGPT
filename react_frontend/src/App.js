import React, {useState} from 'react';
import {ThemeProvider, createTheme} from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import DarkModeToggle from './components/DarkModeToggle';
import FastGPTChat from './components/FastGPTChat';

function App() {
  const [darkMode, setDarkMode] = useState(true);

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
        <Box sx={{flex: 1, textAlign: 'center'}}>
          <Typography variant="h6">Welcome to FastGPT</Typography>
        </Box>
        <DarkModeToggle onChange={handleThemeChange} checked={darkMode}/>
      </Box>
      <FastGPTChat/>
    </ThemeProvider>
  );
}

export default App;
