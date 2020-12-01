import React, { useState, useEffect } from 'react';

import Plot from 'react-plotly.js'; 
import styled from 'styled-components';
import Axios from 'axios'; 

const S = {
  Wrapper: styled.section`
    width: 100%;
    
    display: flex;
    flex-direction: column;
    align-items: center;
  `,
  Description: styled.p`
    ${(props) => props.theme.typography.description};
    font-size: 1rem;
  `,
};

const GenderCumulGraph = () => {

  const cumulDomesticState = { 
    data: [], 
    layout: {}
  }
  const [cumulData, setCumulData] = useState(cumulDomesticState);

  useEffect(() => {
    Axios.get("/api/domestic-cumul-plotly", { 
        params: { 
          query: 'gender'
        } 
      })
      .then(response => {
        setCumulData({
          data: response.data.data, 
          layout: response.data.layout
        })
    })
  }, []);

  
  return (
    <S.Wrapper>
      <div className='row'>
        <div className='plot-plotly col-md-auto'>
          <Plot 
            data={cumulData.data} 
            layout={cumulData.layout}
          />
        </div>
      </div>
    </S.Wrapper>
  );
};

export default GenderCumulGraph;
