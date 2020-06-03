import React from 'react';
import './App.css';
import { Colour, PieceComponent } from './Piece'
import { LocationComponent } from './Location'
import { DieComponent } from './Die'


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
        this.handleClick = this.handleClick.bind(this)
    }

    private async movePiece(location: number, dieRoll: number) {
        try {
            const response = await fetch(`http://localhost:5000/move-piece?location=${location}&die-roll=${dieRoll}`)
            const result = await response.json()
            this.setState({
                piecesByLocation: JSON.parse(result.board),
                diceRoll: result.dice_roll
            })
        }
        catch {
            console.log('This move is not allowed')
        }

    }

    private async handleClick() {
        const response = await fetch("http://localhost:5000/new-game")
        const result = await response.json()
        this.setState({
            piecesByLocation: JSON.parse(result.board),
            diceRoll: result.dice_roll
        })
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

        // Taken location is the centre of the board
        if (location === 0 ) {
            xpos = 46.5
            ypos = 40 - y_sep * i
        } else if (location === 25) {
            xpos = 46.5
            ypos = 50 + y_sep * i
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
            xpos = x0_left + x_sep * (index - 1)
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

        // These are when the home pieces will go
        if (location === 0 || location === 25) {
            xpos += 3
        }
        // Positions of the top left of the zone
        return [xpos, ypos]
    }

    private async handlePieceDrop(locationStart: number, locationEnd: number) {
        console.log(locationStart)
        console.log(locationEnd)
        let dieRoll = Math.abs(locationEnd - locationStart)
        await this.movePiece(locationStart, dieRoll)
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
                    onDrop={async newLocation => {
                        await this.handlePieceDrop(+location, newLocation)
                    }}
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

    private renderDice() {
        let dice = []
        for (let i = 0; i < this.state.diceRoll.length; i++) {
            let position = [4 + 8*(i + 1), 45]
            dice.push(<DieComponent
                xposition={position[0]}
                yposition={position[1]}
                roll={this.state.diceRoll[i]}
                key={`dice-${i}`}
            ></DieComponent>)
        }
        return dice
    }

    render() {
        return (
            <div className='board' id='board'>
                {this.renderZones()}
                {this.renderPieces()}
                {this.renderDice()}
                <button onClick={this.handleClick}> New Game </button>
            </div>
        )
    }
}
