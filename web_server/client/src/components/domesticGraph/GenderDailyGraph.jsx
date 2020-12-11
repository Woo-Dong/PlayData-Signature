import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import styled from 'styled-components';
import Axios from 'axios'; 

const S = {
  Wrapper: styled.section`
    width: 100%;
    padding-top: 60px;
    padding-bottom: 30px;
    
    display: flex;
    flex-direction: column;
    align-items: center;
  `,
  Title: styled.h1`
    ${props => props.theme.typography.title};
    color: #f1c232;
    margin-bottom: 0.5rem;
    
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

const GenderDailyGraph = () => {

  const dailyDomesticState = { 
    data: [], 
    layout: {}, 
    maximum: '', 
    mimimum: ''
  }
  const [dailyData, setDailyData] = useState(dailyDomesticState);


  useEffect(() => {
    Axios.get("/api/domestic-daily-plotly", { 
        params: { 
          query: 'gender', 
          y: 'confirmed'
        } 
      })
      .then(response => {
        setDailyData({
          data: response.data.data, 
          layout: response.data.layout,
          maximum: response.data.maximum, 
          minimum: response.data.minimum
        })
    })
  }, []);

  
  return (
    <S.Wrapper>
      <S.Title >국내 상황</S.Title>
      <S.Label >확진자 현황</S.Label>
      <S.Label >성별 분석</S.Label>
      <div className='row'>
        <div className='plot-plotly col-md-auto'>
          <Plot 
            data={dailyData.data} 
            layout={dailyData.layout}
          />
          <S.Description>
            7일간 최대 확진자 그룹 =&gt; {dailyData.maximum}
            <br /> 
            7일간 최소 확진자 그룹 =&gt; {dailyData.minimum}
          </S.Description>
        </div>
      </div>
    </S.Wrapper>
  );
};

export default GenderDailyGraph;
