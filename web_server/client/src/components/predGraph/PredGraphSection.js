import React from 'react';

import PredGraph from './PredGraph';


export default class PredGraphSection extends React.Component {
  constructor(props) {
    super(props);
    this.mainStyles = { 
      // backgroundImage: props.backgroundImage,
      // backgroundSize: "cover",
      // backgroundPosition: "top center",
      // backgroundColor: "rgba( 255, 255, 0, 0.1 )",
      // minHeight: "1100px"
    }
  }

  render() {
    return (
      <div className="section" style={this.mainStyles}>
        <PredGraph />
      </div>
    );
  }
}

