import React from 'react';
import GlobalGraphCumul from './GlobalGraphCumul'; 
import GlobalGraphDaily from './GlobalGraphDaily'; 



export default class GlobalGraphSection extends React.Component {
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
      <div className="graph_section" style={this.mainStyles}>
        <div className="row">
          <GlobalGraphDaily />
          <GlobalGraphCumul /> 
        </div>
      </div>
    );
  }
}

