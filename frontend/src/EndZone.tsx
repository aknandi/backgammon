import React from 'react';
import { Colour } from './Piece'
import './EndZone.css';

import interact from 'interactjs'
// import '@interactjs/types'

type Props = {
    colour: Colour,
    xposition: number,
    yposition: number,
    piecesCount: number,
}

export class EndZoneComponent extends React.Component<Props, {}> {
    private domElement: React.RefObject<HTMLDivElement> = React.createRef<HTMLDivElement>();

    constructor(props: any) {
        super(props);
        this.state = {}
    }

    componentDidMount() {
        interact(this.domElement.current!)
            .dropzone({
                accept: '.piece',
                overlap: 0.5,
            });
    }

    private renderPieces() : JSX.Element[] {
        let pieces = []
        for (let i = 0; i<this.props.piecesCount; i++) {
            pieces.push(<div className='end-piece' key={i} style={{backgroundColor: this.props.colour}}/>)
        }
        return pieces
    }

    render() {
        return (
            <div className='endzone' ref={this.domElement} style={this.setStyle()} id={this.props.colour === Colour.Black ? "0" : "25"} >
                <div className='end-pieces'>{this.renderPieces()}</div>
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