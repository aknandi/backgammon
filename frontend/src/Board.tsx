import React from 'react';
import './App.css';
import { Colour, PieceComponent } from './Piece'
import { LocationComponent } from './Location'
import { DieComponent } from './Die'
import { EndZoneComponent } from './EndZone'

import audioOn from './audioOn.svg'
import audioOff from './audioOff.svg'

import Cookies from "js-cookie"

async function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

type State = {
    piecesByLocation: { [location: number]: { colour: Colour, count: number } },
    diceRoll: number[],
    usedRolls: number[],
    winner: Colour | null,
    computersGo: boolean,
    playerCanMove: boolean,
    muted: boolean,
    difficultly: string,
    showNewGameModal: boolean,
}

export class BoardComponent extends React.Component<{}, State> {

    private readonly backendurl = 'http://localhost:5000'
    private readonly audioDiceRoll = new Audio(`${process.env.PUBLIC_URL}/dice-roll.mp3`);
    private readonly audioPieceMove = new Audio(`${process.env.PUBLIC_URL}/piece-move.mp3`);
    constructor(props: any) {
        super(props);
        this.state = {
            piecesByLocation: {},
            diceRoll: [],
            usedRolls: [],
            winner: null,
            computersGo: false,
            playerCanMove: true,
            muted: Boolean(Cookies.get('muted')) ?? false,
            difficultly: Cookies.get('difficulty') ?? 'veryhard',
            showNewGameModal: false,
        }
        this.handleNewGameClick = this.handleNewGameClick.bind(this)
        this.handleDifficultyChange = this.handleDifficultyChange.bind(this);
        this.handleModalConfirmClick = this.handleModalConfirmClick.bind(this);
        this.handleExitModalClick = this.handleExitModalClick.bind(this);
    }

    private playDiceRollSound() {
        if (!this.state.muted) {
            this.audioDiceRoll.play();
        }
    }

    private playPieceMoveSound() {
        if (!this.state.muted) {
            this.audioPieceMove.play();
        }
    }

    private async movePiece(location: number, dieRoll: number, endTurn: boolean = false) {
        try {
            const response = await fetch(`${this.backendurl}/move-piece?location=${location}&die-roll=${dieRoll}&end-turn=${endTurn}`)
            const result = await response.json()
            if (result.opp_move) {
                this.playPieceMoveSound();
                this.setState({
                    piecesByLocation: JSON.parse(result.board_after_your_last_turn),
                    diceRoll: [],
                    usedRolls: [],
                });
                await sleep(750);
                this.playDiceRollSound();
                this.setState({
                    diceRoll: [0, 0],
                    usedRolls: [],
                    computersGo: true,
                });
                await sleep(1000);
                this.setState({
                    diceRoll: result.opp_roll,
                });
                await sleep(2000);
                for (let i = 0; i < result.opp_move.length; i++) {
                    let move = result.opp_move[i];
                    this.playPieceMoveSound();
                    this.setState({
                        piecesByLocation: JSON.parse(move.board_after_move),
                        usedRolls: [...this.state.usedRolls, move.die_roll],
                    });
                    await sleep(2000);
                }
                if (result.winner == null) {
                    this.playDiceRollSound();
                    this.setState({
                        diceRoll: [0, 0],
                        usedRolls: [],
                    });
                    await sleep(1000);
                }
            } else if (result.result === "success") {
                this.playPieceMoveSound();
            }
            this.setState({
                piecesByLocation: JSON.parse(result.board),
                diceRoll: result.dice_roll,
                usedRolls: result.used_rolls,
                winner: result.winner,
                computersGo: false,
            });

            if (!result.player_can_move && this.state.winner == null) {
                this.setState({
                    playerCanMove: false,
                    computersGo: true,
                })
                await sleep(3000)
                this.setState({
                    playerCanMove: true,
                })
                this.movePiece(0, 0, true)
            }
        }
        catch (e) {
            console.log(e)
        }
    }

    private async handleNewGameClick() {
        this.setState({
            showNewGameModal: true
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
            y_sep = max_height / count
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
        if (location === 0) {
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

        let diceRollsLeft = [...this.state.diceRoll]
        for (let i = 0; i < this.state.usedRolls.length; i++) {
            let roll = this.state.usedRolls[i]
            const index = diceRollsLeft.indexOf(roll);
            diceRollsLeft.splice(index, 1);
        }

        let dieRoll = Math.abs(locationEnd - locationStart)
        if (locationEnd === 25 && !diceRollsLeft.includes(dieRoll) && dieRoll < Math.max(...diceRollsLeft)) {
            dieRoll = Math.min(...diceRollsLeft.filter(x => x > dieRoll))
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
                let canMove = !this.state.computersGo && colourAtLocation === Colour.White
                pieces.push(<PieceComponent
                    colour={colourAtLocation}
                    xposition={position[0]}
                    yposition={position[1]}
                    key={`${location}-${i}-${canMove}`}
                    onDrop={async newLocation => {
                        await this.handlePieceDrop(+location, newLocation)
                    }}
                    isMoveable={canMove}
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
            let position = [1 + 8 * (i + 1), 46]
            let roll = this.state.diceRoll[i]
            let used = false;
            if (usedRolls.includes(roll)) {
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

    private getPieceCount(colour: Colour): number {
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
            return <div className='winner'>{this.state.winner === Colour.White ? "You won :)" : "You lost :("} </div>
        }
    }

    private renderNoMoreMoves() {
        if (!this.state.playerCanMove) {
            return <div className='cantmove'>You can't move :( </div>
        }
    }

    private handleMuteClick() {
        let newValue = !this.state.muted
        if(newValue) {
            Cookies.set('muted', 'true')
        } else {
            Cookies.remove('muted')
        }
        this.setState({
            muted: newValue,
        })
    }

    private renderDifficultyMenu() {
        return (
            <div>
                <select className='strategy-select' value={this.state.difficultly} onChange={this.handleDifficultyChange} name="strategy">
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                    <option value="veryhard">Very Hard</option>
                </select>
            </div>
        )
    }

    private handleDifficultyChange(event: any) {
        this.setState({
            difficultly: event.target.value
        });
    }

    private async handleModalConfirmClick() {
        Cookies.set('difficulty', this.state.difficultly)
        const response = await fetch(`${this.backendurl}/new-game?difficulty=${this.state.difficultly}`)
        const result = await response.json()
        this.setState({
            piecesByLocation: JSON.parse(result.board),
            diceRoll: result.dice_roll,
            usedRolls: result.used_rolls,
            winner: result.winner,
            showNewGameModal: false,
        })
    }

    private handleExitModalClick() {
        this.setState({
            showNewGameModal: false,
        })
    }

    private renderModal() {
        if (this.state.showNewGameModal) {
            return <div className="modal">
                <div className="modal-content">
                    <button className="close" onClick={this.handleExitModalClick}>&times;</button>
                    <p>Are you sure you want to start a new game?</p>
                    <p>Select the difficulty</p>
                    {this.renderDifficultyMenu()}
                    <br></br>
                    <button className='modalbutton' onClick={this.handleModalConfirmClick}> Start New Game </button>
                </div>
            </div>
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
                {this.renderNoMoreMoves()}
                {this.renderModal()}
                <button className='newgamebutton' onClick={this.handleNewGameClick}> New Game </button>
                <img className='mutebutton' src={this.state.muted === true ? audioOff : audioOn} onClick={() => this.handleMuteClick()} alt='mute' />
            </div>
        )
    }
}
