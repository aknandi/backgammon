import React from 'react';
import './Location.css';

import interact from 'interactjs'
// import '@interactjs/types'

type Props = {
  xposition: number,
  yposition: number,
  location: number,
}

export class LocationComponent extends React.Component<Props, {}> {
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

  render() {
    return (
      <div className='location' ref={this.domElement} style={this.setStyle()} id={`${this.props.location}`} />
    )
  }

  private setStyle(): React.CSSProperties {
    return {
      left: `${this.props.xposition}%`,
      top: `${this.props.yposition}%`
    };
  }
}