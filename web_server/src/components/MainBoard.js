import React from 'react';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import DashBoard from './DashBoard';


export default class MainBoard extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="section">
        <DashBoard /> 
      </div>
    );
  }
}

