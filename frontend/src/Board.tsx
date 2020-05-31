import React from 'react';
import './App.css';
import { Colour, PieceComponent } from './Piece'

type State = {
    piecesByLocation: { [location: number]: { colour: Colour, count: number } }
}

export class BoardComponent extends React.Component<{}, State> {

    constructor(props: any) {
        super(props);
        this.state = {
            piecesByLocation: {},
        }
    }

    componentDidMount() {
        fetch("http://localhost:5000/start-game")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        piecesByLocation: result
                    });
                },
            )
    }

    private locationToPosition(location: number, i: number): [number, number] {

        let index, xpos, ypos
        let x_sep = 7.2
        let y_sep = 8.8
        if (location < 7) { // bottom right
            index = 7 - location
            xpos = 52.5 + x_sep * (index - 1)
            ypos = 87.0 - y_sep * i
        } else if (location < 13) { // bottom left
            index = 13 - location
            xpos = 4.3 + x_sep * (index - 1)
            ypos = 87.0 - y_sep * i
        } else if (location < 19) { // top left
            index = location - 12
            xpos = 4.3 + x_sep * (index - 1)
            ypos = 2.6 + y_sep * i
        } else { // top right
            index = location - 18
            xpos = 52.5 + x_sep * (index - 1)
            ypos = 2.6 + y_sep * i
        }
        return [xpos, ypos]
        // Need to convert python positions 0 to 25 to css x and y positions
    }

    private renderPieces() {
        let pieces = []
        //let locations = Object.keys(this.state.piecesByLocation)
        for (let location of Object.keys(this.state.piecesByLocation)) {
            let colourAtLocation = this.state.piecesByLocation[+location].colour
            for (let i = 0; i < this.state.piecesByLocation[+location].count; i++) {
                let position = this.locationToPosition(+location, i)
                pieces.push(<PieceComponent 
                    colour={colourAtLocation} 
                    xposition={position[0]} 
                    yposition={position[1]}
                    key={`${location}-${i}`}
                ></PieceComponent>)
            }
        }
        return pieces
    }

    render() {
        return (
            <div className='board'>
                {this.renderPieces()}
            </div>
        )
    }
}
