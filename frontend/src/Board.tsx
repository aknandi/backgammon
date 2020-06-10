import React from 'react';
import './App.css';
import { Colour, PieceComponent } from './Piece'
import { LocationComponent } from './Location'
import { DieComponent } from './Die'
import { EndZoneComponent } from './EndZone'

async function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

type State = {
    piecesByLocation: { [location: number]: { colour: Colour, count: number } },
    diceRoll: number[],
    usedRolls: number[],
    winner: Colour | null,
}

export class BoardComponent extends React.Component<{}, State> {

    private readonly backendurl = 'http://localhost:5000'
    constructor(props: any) {
        super(props);
        this.state = {
            piecesByLocation: {},
            diceRoll: [],
            usedRolls: [],
            winner: null,
        }
        this.handleClick = this.handleClick.bind(this)
    }

    private async movePiece(location: number, dieRoll: number) {
        try {
            const response = await fetch(`${this.backendurl}/move-piece?location=${location}&die-roll=${dieRoll}`)
            const result = await response.json()
            if(result.opp_move) {
                this.setState({
                    piecesByLocation: JSON.parse(result.board_after_your_last_turn),
                    diceRoll: [0, 0],
                    usedRolls: [],
                });
                await sleep(1500);
                this.setState({
                    diceRoll: result.opp_roll,
                });
                await sleep(2000);
                for(let i = 0; i < result.opp_move.length; i++) {
                    let move = result.opp_move[i];
                    this.setState({
                        piecesByLocation: JSON.parse(move.board_after_move),
                        usedRolls: [...this.state.usedRolls, move.die_roll],
                    });
                    await sleep(2000);
                }
                this.setState({
                    diceRoll: [0, 0],
                    usedRolls: [],
                });
                await sleep(1500);
            }
            this.setState({
                piecesByLocation: JSON.parse(result.board),
                diceRoll: result.dice_roll,
                usedRolls: result.used_rolls,
                winner: result.winner,
            });
        }
        catch {
            console.log('This move is not allowed')
        }

    }

    private async handleClick() {
        if (!window.confirm("Are you sure you want to start a new game?")) {
            return
        } 
        const response = await fetch(`${this.backendurl}/new-game`)
        const result = await response.json()
        this.setState({
            piecesByLocation: JSON.parse(result.board),
            diceRoll: result.dice_roll,
            usedRolls: result.used_rolls,
            winner: result.winner,
        })
    }

    componentDidMount() {
        fetch(`${this.backendurl}/start-game`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        piecesByLocation: JSON.parse(result.board),
                        diceRoll: result.dice_roll,
                        usedRolls: result.used_rolls,
                        winner: result.winner,
                    });
                },
            )
    }

    private locationToPosition(location: number, i: number, count: number): [number, number] {

        let index, xpos, ypos

        let x0_right = 47.5
        let x0_left = 2.45
        let y0_bottom = 87.0
        let y0_top = 2.8

        let x_sep = 6.8
        let y_sep = 8.8
        let max_height = y_sep * 5 - 6.5

        // If the height goes that of 5 pieces start overlapping pieces such that they're always the same height
        if (count > 5) {
            y_sep = max_height/count
        }
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
            xpos = 42.0
            ypos = 40 - y_sep * i
        } else if (location === 25) {
            xpos = 42.0
            ypos = 50 + y_sep * i
        }

        return [xpos, ypos]
        // Need to convert python positions 0 to 25 to css x and y positions
    }

    private getZonePosition(location: number): [number, number] {

        let index, xpos, ypos

        let x0_right = 47;
        let x0_left = 2.2;
        let y_bottom = 49.9;
        let y_top = 3.5;

        let x_sep = 6.9;
        if (location < 7) { // bottom right
            index = 7 - location;
            xpos = x0_right + x_sep * (index - 1);
            ypos = y_bottom;
        } else if (location < 13) { // bottom left
            index = 13 - location;
            xpos = x0_left + x_sep * (index - 1);
            ypos = y_bottom;
        } else if (location < 19) { // top left
            index = location - 12;
            xpos = x0_left + x_sep * (index - 1);
            ypos = y_top;
        } else { // top right
            index = location - 18;
            xpos = x0_right + x_sep * (index - 1);
            ypos = y_top;
        }

        // Positions of the top left of the zone
        return [xpos, ypos]
    }

    private async handlePieceDrop(locationStart: number, locationEnd: number) {
        console.log(locationStart)
        console.log(locationEnd)
        let dieRoll = Math.abs(locationEnd - locationStart)
        if (locationEnd === 25 && !this.state.diceRoll.includes(dieRoll) && dieRoll < Math.max(...this.state.diceRoll)) {
            dieRoll = Math.min(...this.state.diceRoll.filter(x => x > dieRoll))
        }
        await this.movePiece(locationStart, dieRoll)
    }

    private renderPieces() {
        let pieces = []
        let locations = this.state.piecesByLocation
        for (let location of Object.keys(locations)) {
            let colourAtLocation = locations[+location].colour
            for (let i = 0; i < locations[+location].count; i++) {
                let position = this.locationToPosition(+location, i, locations[+location].count)
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
        for (let location = 1; location <= 24; location++) {
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
        let usedRolls = [...this.state.usedRolls]
        for (let i = 0; i < this.state.diceRoll.length; i++) {
            let position = [1 + 8*(i + 1), 46]
            let roll = this.state.diceRoll[i]
            let used = false;
            if(usedRolls.includes(roll)) {
                used = true
                const index = usedRolls.indexOf(roll);
                usedRolls.splice(index, 1);
            }
            dice.push(<DieComponent
                xposition={position[0]}
                yposition={position[1]}
                roll={roll}
                used={used}
                key={`dice-${i}`}
            ></DieComponent>)
        }
        return dice
    }

    private getPieceCount(colour : Colour) : number {
        let numberOfPieces = 0
        for (let location of Object.keys(this.state.piecesByLocation)) {
            if (this.state.piecesByLocation[+location].colour === colour) {
                numberOfPieces += this.state.piecesByLocation[+location].count
            }
        }
        return numberOfPieces
    }

    private renderWinner() {
        if (this.state.winner) {
            return <div className='winner'>{this.state.winner === Colour.White ? "You won :)": "You lost :("} </div>
        }
    }

    render() {
        return (
            <div className='board' id='board'>
                {this.renderZones()}
                {this.renderPieces()}
                {this.renderDice()}
                <EndZoneComponent
                    colour={Colour.White}
                    xposition={92}
                    yposition={3.5}
                    piecesCount={15 - this.getPieceCount(Colour.White)}
                    />
                <EndZoneComponent
                    colour={Colour.Black}
                    xposition={92}
                    yposition={52.8}
                    piecesCount={15 - this.getPieceCount(Colour.Black)}
                    />
                {this.renderWinner()} 
                <button className='newgamebutton' onClick={this.handleClick}> New Game </button>
            </div>
        )
    }
}
