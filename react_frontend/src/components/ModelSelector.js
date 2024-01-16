import React, {useState, useEffect} from 'react';
import {Select, MenuItem, FormControl, InputLabel} from '@mui/material';

const ModelSelector = () => {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/models')
      .then(response => response.json())
      .then(data => setModels(data.models))
      .catch(error => {
        console.error('Error fetching models:', error);
      });
  }, []);

  const handleModelChange = (event) => {
    setSelectedModel(event.target.value);
  };

  return (
    <FormControl>
      <InputLabel id="model-selector-label">Model</InputLabel>
      <Select
        labelId="model-selector-label"
        value={selectedModel}
        onChange={handleModelChange}
        displayEmpty
      >
        <MenuItem value="">
          <em></em>
        </MenuItem>
        {models.map((model) => (
          <MenuItem key={model} value={model}>{model}</MenuItem>
        ))}
      </Select>
    </FormControl>
  )
}

export default ModelSelector;