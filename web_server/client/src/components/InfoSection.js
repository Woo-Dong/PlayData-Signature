import React from 'react';
import Info from './Info';


export default class InfoSection extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="section">
        <Info /> 
      </div>
    );
  }
}

