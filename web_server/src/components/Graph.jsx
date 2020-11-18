import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import { useScrollFadeIn } from '../hooks';
import styled from 'styled-components';
import Axios from 'axios'; 

const S = {
  Wrapper: styled.section`
    width: 100%;
    padding: 120px 0;
    
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

const Graph = () => {
  const animatedItem = {
    0: useScrollFadeIn('up',     1,   0, 0.5),
    1: useScrollFadeIn('up',     1, 0.3, 0.5),
    2: useScrollFadeIn('left', 0.5, 0.6, 0.5),
    3: useScrollFadeIn('up',     1, 0.9, 0.5),
		4: useScrollFadeIn('left', 0.5, 1.2, 0.5),
  };

  const valDataState = { 
    data: [], 
    layout: {}
  }

  const predDataState = { 
    data: [], 
    layout: {}
  }

  const [valData, setValData] = useState(valDataState);
  const [predData, setPredData] = useState(predDataState); 


  useEffect(() => {
    // Axios.get("http://localhost:5000/api/validate-fbprophet-plotly")
    Axios.get("/api/validate-fbprophet-plotly")
      .then(response => {
        setValData({
          data: response.data.data, 
          layout: response.data.layout
        })
      
        
    })

    // Axios.get("http://localhost:5000/api/predict-fbprophet-plotly")
    Axios.get("/api/predict-fbprophet-plotly")
      .then(response => {
        setPredData({
          data: response.data.data, 
          layout: response.data.layout
        })
    })

  }, []);

  
  return (
    <S.Wrapper>
      <S.Label {...animatedItem[0]}>COVID-19 확진자 그래프</S.Label>
      <S.Label {...animatedItem[1]}>
        지난 7일간 예측 값과 실제 값 비교
      </S.Label>
      <br />
      
      <div className='row'>
        <div className='plot-plotly col-md-auto' {...animatedItem[2]}>
          <Plot 
            data={valData.data} 
            layout={valData.layout}
          />
          <S.Description>
            평균 오차: {}
            <br/>
            최소 오차: {} 
            최대 오차: {}
          </S.Description>
        </div>
      </div>

      <S.Label {...animatedItem[3]}>
        향후 7일간 예측 결과
      </S.Label>
      <br />
      
      <div className='row'>
        <div className='plot-plotly col-md-auto' {...animatedItem[4]}>
          <Plot 
            data={predData.data} 
            layout={predData.layout}
          />
          <S.Description>
            평균 오차: {}
            <br/>
            최소 오차: {} 
            최대 오차: {}
          </S.Description>
        </div>
      </div>
      
    </S.Wrapper>
  );
};

export default Graph;
