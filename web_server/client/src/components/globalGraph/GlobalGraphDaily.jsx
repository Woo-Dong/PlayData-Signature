import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import styled from 'styled-components';
import Axios from 'axios'; 

const S = {
  Wrapper: styled.section`
    width: 100%;
    padding-top: 60px; 
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
  Title: styled.h2`
    ${props => props.theme.typography.subtitle};
    color: ${props => props.theme.palette.black};
    margin-bottom: 2rem;
    text-align: center;
  `,
  Description: styled.p`
    ${(props) => props.theme.typography.description};
    font-size: 1rem;
  `,
};

const GlobalGraphDaily = () => {

  const dailyGlobalState = { 
    data: [], 
    layout: {}
  }
  const [dailyGlobal, setDailyGlobal] = useState(dailyGlobalState);

  useEffect(() => {
    Axios.get("/api/global-daily-plotly")
      .then(response => {
        setDailyGlobal({
          data: response.data.data, 
          layout: response.data.layout
        })
    })
  }, []);

  
  return (
    <S.Wrapper>
      <S.Label >GLOBAL COVID-19 확진자 그래프</S.Label>
      <S.Label >
        일별 상황
      </S.Label>
      <br />
      <div className='row'>
        <div className='plot-plotly col-md-auto'>
          <Plot 
            data={dailyGlobal.data} 
            layout={dailyGlobal.layout}
          />
        </div>
      </div>
    </S.Wrapper>
  );
};

export default GlobalGraphDaily;
