import React from 'react';
import './Piece.css';
import whitePiece from './white-piece.svg'
import blackPiece from './black-piece.svg'

type Props = {
  colour: Colour,
  xposition: number,
  yposition: number,
}

export enum Colour {
  White = "white",
  Black = "black",
}

export class PieceComponent extends React.Component<Props, {}> {

  constructor(props: any) {
    super(props);
    this.state = {}
  }

  render() {
    return (
      <div className='piece' style={this.setStyle()}>
        <img src={this.props.colour === Colour.White ? whitePiece : blackPiece} alt="white-piece" />
      </div>
    )
  }

  private setStyle(): React.CSSProperties {
    return { 
      left: `${this.props.xposition}%`,
      top: `${this.props.yposition}%` };
  }
}