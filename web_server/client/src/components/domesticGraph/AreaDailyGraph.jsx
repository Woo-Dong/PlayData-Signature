import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import styled from 'styled-components';
import Axios from 'axios'; 

const S = {
  Wrapper: styled.section`
    width: 100%;
    padding-top: 120px;
    padding-bottom: 60px;
    
    display: flex;
    flex-direction: column;
    align-items: center;
  `,
  Label: styled.p`
    display: inline-block;
    ${props => props.theme.typography.label};
    color: ${props => props.theme.palette.primary};
    margin-bottom: 1rem;
  `,
  Description: styled.p`
    ${(props) => props.theme.typography.description};
    font-size: 1rem;
  `,
};

const AreaDailyGraph = () => {

  const dailyDomesticState = { 
    data: [], 
    layout: {}
  }
  const [dailyData, setDailyData] = useState(dailyDomesticState);


  useEffect(() => {
    Axios.get("/api/domestic-daily-plotly", { 
        params: { 
          query: 'area', 
          y: 'confirmed'
        } 
      })
      .then(response => {
        setDailyData({
          data: response.data.data, 
          layout: response.data.layout
        })
    })
  }, []);

  
  return (
    <S.Wrapper>
      <S.Label >Domestic COVID-19 확진자 그래프</S.Label>
      <S.Label >
        지역별 분석
      </S.Label>
      <div className='row'>
        <div className='plot-plotly col-md-auto'>
          <Plot 
            data={dailyData.data} 
            layout={dailyData.layout}
          />
        </div>
      </div>
    </S.Wrapper>
  );
};

export default AreaDailyGraph;
