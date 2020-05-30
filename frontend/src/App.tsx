import React from 'react';
import backgammonBoard from './backgammon-board.gif';
import whitePiece from './white-piece.svg'
import blackPiece from './black-piece.svg'
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={backgammonBoard} className="board" alt="logo" />
        <img src={whitePiece} className="board" alt="logo" />
        <img src={blackPiece} className="board" alt="logo" />
      </header>
    </div>
  );
}

export default App;
