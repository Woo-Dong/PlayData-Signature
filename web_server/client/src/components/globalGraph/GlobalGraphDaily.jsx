import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import { useScrollFadeIn } from '../../hooks';
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
  Title: styled.h1`
    ${props => props.theme.typography.title};
    color: #f1c232;
    margin-bottom: 0.5rem;
  `,
  Description: styled.p`
    ${(props) => props.theme.typography.description};
    font-size: 1rem;
  `,
};

const GlobalGraphDaily = () => {

  const animatedItem = {
    0: useScrollFadeIn('up',     1,   0, 0.5),
    1: useScrollFadeIn('up',     1, 0.3, 0.5),
    2: useScrollFadeIn('left', 0.5, 0.6, 0.5),
  };

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
      <S.Title {...animatedItem[0]}>세계 상황</S.Title>
      <S.Label {...animatedItem[1]}>
        일별 상황
      </S.Label>
      <br />
      <div className='row'>
        <div className='plot-plotly col-md-auto' {...animatedItem[2]}>
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
