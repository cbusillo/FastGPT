import React from 'react';
import Switch from '@mui/material/Switch';

const DarkModeToggle = ({onChange, checked}) => {
  return (
    <Switch
      checked={checked}
      onChange={onChange}
      name="darkMode"
      inputProps={{'aria-label': 'dark mode toggle'}}
    />
  );
};

export default DarkModeToggle;