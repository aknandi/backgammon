import React from 'react';
import './Piece.css';
import whitePiece from './white-piece.svg'
import blackPiece from './black-piece.svg'

import interact from 'interactjs'
// import '@interactjs/types'

type Props = {
  colour: Colour,
  xposition: number,
  yposition: number,
  onDrop: (location: number) => Promise<void>,
}

export enum Colour {
  White = "white",
  Black = "black",
}

export class PieceComponent extends React.Component<Props, {}> {
  private domElement: React.RefObject<HTMLDivElement> = React.createRef<HTMLDivElement>();

  constructor(props: any) {
    super(props);
    this.state = {}
  }

  componentDidMount() {
    interact(this.domElement.current!)
      .draggable({
        inertia: false,
        modifiers: [
          interact.modifiers.restrictRect({
            restriction: '#backgammon',
            endOnly: true
          })
        ],
        autoScroll: true,
        listeners: {
          move: dragMoveListener,
          end: async (event) => {
            let location = event.dropzone?.target?.id;
          await this.props.onDrop(location);
            // Remove the tranformation
            event.target.style.transform = ''
            event.target.setAttribute('data-x', null)
            event.target.setAttribute('data-y', null)
          }
        }
      });

    function dragMoveListener(event: any) {
      var target = event.target
      // keep the dragged position in the data-x/data-y attributes
      var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
      var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy

      // translate the element
      target.style.webkitTransform =
        target.style.transform =
        'translate(' + x + 'px, ' + y + 'px)'

      // update the posiion attributes
      target.setAttribute('data-x', x)
      target.setAttribute('data-y', y)
    }
  }

  render() {
    return (
      <div className='piece' ref={this.domElement} style={this.setStyle()}>
        <img src={this.props.colour === Colour.White ? whitePiece : blackPiece} alt="white-piece" />
      </div>
    )
  }

  private setStyle(): React.CSSProperties {
    return {
      left: `${this.props.xposition}%`,
      top: `${this.props.yposition}%`
    };
  }
}