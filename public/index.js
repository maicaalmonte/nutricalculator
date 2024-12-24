import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // Import your styles if any
import App from './App';  // Import your main App component

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')  // Ensure there's an element with id 'root' in your index.html
);
