import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import { useScrollFadeIn } from '../../hooks';

import styled from 'styled-components';
import Axios from 'axios'; 

const S = {
  Wrapper: styled.section`
    width: 100%;
    padding-top: 60px;
    
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

const GlobalGraphCumul = () => {

  const animatedItem = {
    0: useScrollFadeIn('up',     1,   0, 0.5),
		1: useScrollFadeIn('left', 0.5, 0.6, 0.5),
  };

  const cumulGlobalState = { 
    data: [], 
    layout: {}
  }
  const [cumulGlobal, setCumulGlobal] = useState(cumulGlobalState); 

  useEffect(() => {
    Axios.get("/api/global-cumul-plotly")
      .then(response => {
        setCumulGlobal({
          data: response.data.data, 
          layout: response.data.layout
        })
    })
  }, []);

  
  return (
    <S.Wrapper>
      <S.Label {...animatedItem[0]} >
        누적 상황
      </S.Label>
      <br />
      <div className='row'>
        <div className='plot-plotly col-md-auto' {...animatedItem[1]}>
          <Plot 
            data={cumulGlobal.data} 
            layout={cumulGlobal.layout}
          />
        </div>
      </div>
    </S.Wrapper>
  );
};

export default GlobalGraphCumul;
