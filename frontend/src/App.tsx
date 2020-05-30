import React from 'react';
import backgammon_board from './backgammon_board.gif';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={backgammon_board} className="board" alt="logo" />
      </header>
    </div>
  );
}

export default App;
