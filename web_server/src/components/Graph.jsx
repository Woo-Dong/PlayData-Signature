import React from 'react';
import styled from 'styled-components';
import { useScrollFadeIn } from '../hooks';
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

function plotTest1() { 
    Axios.get("/api/plot1").then(res => window.Bokeh.embed.embed_item(res.data, 'testPlot1'))
}
plotTest1();
Axios.get("/api/plot2").then(res => window.Bokeh.embed.embed_item(res.data, 'testPlot2'))

const Graph = () => {
  const animatedItem = {
    0: useScrollFadeIn('up', 1, 0, 0.5),
    1: useScrollFadeIn('up', 1, 0.1, 0.5),
		2: useScrollFadeIn('left', 0.5, 0.3, 0.4),
		3: useScrollFadeIn('left', 0.5, 0.4, 0.4),
  };

  return (
    <S.Wrapper>
      <S.Label {...animatedItem[0]}>확진자 그래프</S.Label>
      <S.Title {...animatedItem[1]}>
        자료 출처
        <br />
        <S.Description>질병 관리 본부</S.Description>
      </S.Title>
      <div className='row'>
        <div id='testPlot1' className="bk-root1 col-md-auto" {...animatedItem[2]} />
        <div id='testPlot2' className="bk-root2 col-md-auto" {...animatedItem[3]} />
      </div>
    </S.Wrapper>
  );
};

export default Graph;
