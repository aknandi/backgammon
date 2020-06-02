import React from 'react';
import './App.css';
import { Colour, PieceComponent } from './Piece'
import {LocationComponent} from './Location'


type State = {
    piecesByLocation: { [location: number]: { colour: Colour, count: number } },
    diceRoll: number[]
}

export class BoardComponent extends React.Component<{}, State> {

    constructor(props: any) {
        super(props);
        this.state = {
            piecesByLocation: {},
            diceRoll: [],
        }
    }

    private async movePiece(location: number, dieRoll: number) {
        try {
            const response = await fetch(`http://localhost:5000/move-piece?location=${location}&die-roll=${dieRoll}`)
            const json = await response.json()
            this.setState({
                piecesByLocation: json
            })
        }
        catch {
            console.log('This move is not allowed')
        }

    }   

    componentDidMount() {
        (window as any).movePiece = this.movePiece.bind(this);
        fetch("http://localhost:5000/start-game")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        piecesByLocation: JSON.parse(result.board),
                        diceRoll: result.dice_roll
                    });
                },
            )
    }

    private locationToPosition(location: number, i: number): [number, number] {

        let index, xpos, ypos

        let x0_right = 52.5
        let x0_left = 3.0
        let y0_bottom = 84.5
        let y0_top = 6.2

        let x_sep = 7.4
        let y_sep = 8.0 
        if (location < 7) { // bottom right
            index = 7 - location
            xpos = x0_right + x_sep * (index - 1)
            ypos = y0_bottom - y_sep * i
        } else if (location < 13) { // bottom left
            index = 13 - location
            xpos = x0_left + x_sep * (index - 1)
            ypos = y0_bottom - y_sep * i
        } else if (location < 19) { // top left
            index = location - 12
            xpos = x0_left + x_sep * (index - 1)
            ypos = y0_top + y_sep * i
        } else { // top right
            index = location - 18
            xpos = x0_right + x_sep * (index - 1)
            ypos = y0_top + y_sep * i
        }
        return [xpos, ypos]
        // Need to convert python positions 0 to 25 to css x and y positions
    }

    private getZonePosition(location: number): [number, number] {

        let index, xpos, ypos
        
        let x0_right = 52.5
        let x0_left = 3.0
        let y_bottom = 50
        let y_top = 6.2

        let x_sep = 7.4
        if (location < 7) { // bottom right
            index = 7 - location
            xpos = x0_right + x_sep * (index - 1)
            ypos = y_bottom
        } else if (location < 13) { // bottom left
            index = 13 - location
            xpos = x0_left+ x_sep * (index - 1)
            ypos = y_bottom
        } else if (location < 19) { // top left
            index = location - 12
            xpos = x0_left + x_sep * (index - 1)
            ypos = y_top
        } else { // top right
            index = location - 18
            xpos = x0_right + x_sep * (index - 1)
            ypos = y_top
        }

        // Adjust the taken locations a bit
        if (location === 0 || location === 25) {
            xpos += 3 
        }
        // Positions of the top left of the zone
        return [xpos, ypos]
    }

    private handlePieceDrop(locationStart: number, locationEnd: number) {
        console.log(locationStart)
        console.log(locationEnd)
        let dieRoll = Math.abs(locationEnd - locationStart)
        this.movePiece(locationStart, dieRoll)
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
                    onDrop={newLocation => { this.handlePieceDrop(+location, newLocation) }}
                ></PieceComponent>)
            }
        }
        return pieces
    }

    private renderZones() {
        let zones = []
        for (let location = 0; location <= 25; location++) {
            let position = this.getZonePosition(location)
            zones.push(<LocationComponent
                xposition={position[0]}
                yposition={position[1]}
                location={location}
                key={`zone-${location}`}
            ></LocationComponent>)
        }
        return zones
    }

    render() {
        return (
            <div className='board' id='board'>
                {this.renderZones()}
                {this.renderPieces()}
                <div> {this.state.diceRoll} </div>
            </div>
        )
    }
}
