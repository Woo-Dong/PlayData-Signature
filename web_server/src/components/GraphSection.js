import React from 'react';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import Graph from './Graph';


export default class GraphSection extends React.Component {
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
        <Graph />
      </div>
    );
  }
}
