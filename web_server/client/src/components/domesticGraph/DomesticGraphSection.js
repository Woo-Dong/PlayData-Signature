import React from 'react';

import AgeDailyGraph from './AgeDailyGraph';
import AgeCulumGraph from './AgeCumulGraph'; 

import AreaDailyGraph from './AreaDailyGraph';
import AreaCumulGraph from './AreaCumulGraph';

import GenderDailyGraph from './GenderDailyGraph';
import GenderCumulGraph from './GenderCumulGraph';


export default class DomesticGraphSection extends React.Component {
  constructor(props) {
    super(props);
    this.mainStyles = { 
      // backgroundColor: "rgba( 184, 170, 235, 0.25 )",
    }
  }

  render() {
    return (
      <div className="domestic-daily-section" style={this.mainStyles}>
        <div id="domesticDailyIndicators" className="carousel slide" data-ride="carousel">
          <ol className="carousel-indicators">
            <li data-target="#domesticDailyIndicators" data-slide-to="0" className="active"></li>
            <li data-target="#domesticDailyIndicators" data-slide-to="1"></li>
            <li data-target="#domesticDailyIndicators" data-slide-to="2"></li>
          </ol>
          <div className="carousel-inner domestic-graph">
            <div className="carousel-item domestic-graph active">
              <AgeDailyGraph />
              <AgeCulumGraph /> 
            </div>
            <div className="carousel-item domestic-graph">
              <AreaDailyGraph />
              <AreaCumulGraph /> 
            </div>
            <div className="carousel-item domestic-graph">
              <GenderDailyGraph />
              <GenderCumulGraph /> 
            </div>
          </div>
          <a className="carousel-control-prev" href="#domesticDailyIndicators" role="button" data-slide="prev">
            <span className="carousel-control-prev-icon" ></span>
            <span className="sr-only">Previous</span>
          </a>
          <a className="carousel-control-next" href="#domesticDailyIndicators" role="button" data-slide="next">
            <span className="carousel-control-next-icon" aria-hidden="true"></span>
            <span className="sr-only">Next</span>
          </a>

        </div>
      </div>
      
    );
  }
}

