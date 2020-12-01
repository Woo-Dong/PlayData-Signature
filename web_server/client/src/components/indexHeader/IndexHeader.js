import React from 'react';
import HeaderImg from './HeaderImg';
import DashBoard from './DashBoard'; 

export default class IndexHeader extends React.Component {
  constructor(props) {
    super(props);
    this.mainStyles = { 
      // backgroundColor: "rgba( 0, 0, 0, 0.1 )",
    }
  }

  render() {
    return (
      <div className="header-section" style={this.mainStyles}>
        <div id="mainHeaderIndicators" className="carousel slide" data-ride="carousel">
          <ol className="carousel-indicators">
            <li data-target="#mainHeaderIndicators" data-slide-to="0" className="active"></li>
            <li data-target="#mainHeaderIndicators" data-slide-to="1"></li>
            {/* <li data-target="#mainHeaderIndicators" data-slide-to="2"></li> */}
          </ol>
          <div className="carousel-inner">
            <div className="carousel-item active">
              <HeaderImg />
            </div>
            <div className="carousel-item">
              <DashBoard />
            </div>
          </div>

          <a className="carousel-control-prev" href="#mainHeaderIndicators" role="button" data-slide="prev">
            <span className="carousel-control-prev-icon" ></span>
            <span className="sr-only">Previous</span>
          </a>
          <a className="carousel-control-next" href="#mainHeaderIndicators" role="button" data-slide="next">
            <span className="carousel-control-next-icon" aria-hidden="true"></span>
            <span className="sr-only">Next</span>
          </a>

        </div>
      </div>
      
    );
  }
}

