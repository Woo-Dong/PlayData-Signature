import React from 'react';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import HeaderImg from './HeaderImg';

export default class IndexHeader extends React.Component {
  constructor(props) {
    super(props);
    this.mainStyles = { 
      // backgroundColor: "rgba( 255, 255, 255, 0.1 )",
      height: "780px"
    }
  }

  render() {
    return (
      <div className="section" style={this.mainStyles}>
        <HeaderImg />
      </div>
    );
  }
}

