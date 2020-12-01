import React from 'react';
import NewsBox from './NewsBox';
import BrefingInfo from './BrefingInfo';


export default class NewsSection extends React.Component {
  constructor(props) {
    super(props);
    this.mainStyles = { 
      backgroundImage: props.backgroundImage,
      backgroundSize: "cover",
      backgroundPosition: "top center",
      backgroundColor: "rgba( 255, 255, 0, 0.1 )",
      // minHeight: "1100px"
    }
  }

  render() {
    return (
      <div className="section" style={this.mainStyles}>
        <NewsBox />
        <BrefingInfo />
      </div>
    );
  }
}

