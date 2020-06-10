import React from 'react';
import './Die.css';

import die1 from './die-1.svg'
import die2 from './die-2.svg'
import die3 from './die-3.svg'
import die4 from './die-4.svg'
import die5 from './die-5.svg'
import die6 from './die-6.svg'
import dieRolling from './die-rolling.gif'

type Props = {
    xposition: number,
    yposition: number,
    roll: number,
    used: boolean,
}

export class DieComponent extends React.Component<Props, {}> {

    constructor(props: any) {
        super(props);
        this.state = {}
    }

    private getSrc(): string {
        switch (this.props.roll) {
            case 1:
                return die1
            case 2:
                return die2
            case 3:
                return die3
            case 4:
                return die4
            case 5:
                return die5
            case 6:
                return die6
            case 0:
                return dieRolling
            default:
                throw new Error('Die roll not found')
        }
    }

    render() {
        return (
            <div className={this.getClassName()} style={this.setStyle()} id={`${this.props.roll}`} >
                <img src={this.getSrc()} alt="die" />
            </div>
        )
    }

    private setStyle(): React.CSSProperties {
        return {
            left: `${this.props.xposition}%`,
            top: `${this.props.yposition}%`
        };
    }

    private getClassName() {
        let className = 'die';
        if(this.props.used) {
            className += ' used';
        }
        return className;
    }
}