import React from 'react';
import styled from 'styled-components';
import { useScrollFadeIn, useScrollCount } from '../hooks';

const S = {
  
  Background: styled.section`
    background-color: ${(props) => props.theme.palette.background};
    width: 100%;
  `,
  Wrapper: styled.div`
    width: 100%;
    max-width: 1180px;
    margin: auto;
    padding: 120px 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  `,
  Label: styled.p`
    display: inline-block;
    ${props => props.theme.typography.label};
    color: ${props => props.theme.palette.primary};
    margin-bottom: 1rem;
    text-align: center;
  `,
  Title: styled.h2`
    ${props => props.theme.typography.subtitle};
    color: ${props => props.theme.palette.black};
    margin-bottom: 2rem;
    text-align: center;
  `,
  List: styled.ul`
    display: flex;
  `,
  ListItem: styled.li`
    width: 100%;
    padding: 0 2rem;
    text-align: center;
    &:nth-child(2) {
      border: 4px solid ${(props) => props.theme.palette.white};
      border-top: none;
      border-bottom: none;
    }
  `,
  Number: styled.span`
    ${(props) => props.theme.typography.subtitle};
    color: ${(props) => props.theme.palette.secondary};
    font-size: 3rem;
    margin-bottom: 1rem;
  `,
  Unit: styled.span`
    ${(props) => props.theme.typography.subtitle};
    color: ${(props) => props.theme.palette.secondary};
    font-size: 3rem;
    margin-bottom: 1rem;
  `,
  Title: styled.h4`
    ${(props) => props.theme.typography.subheading};
    margin: 1rem 0;
    text-align: center;
    margin-bottom: 2rem;
  `,
  Description: styled.p`
    ${(props) => props.theme.typography.description};
  `,
  
};

const DashBoard = () => {

  const request = require('sync-request'); 
  const dashData = JSON.parse(request('GET', '/api/dashboard').getBody());
  console.log(dashData); 

  const FIGURE_ITEMS = [
    {
      title: '총 확진자',
      number: dashData.confirmed,
      unit: '',
      description: '---',
    },
    {
      title: '격리해제',
      number: dashData.released,
      unit: '',
      description:
        '---',
    },
    {
      title: '사망자',
      number: dashData.death,
      unit: '',
      description:
        '---',
    },
  ];

  const FIGURE_ITEMS2 = [
    {
      title: '총 확진자',
      number: dashData.today_confirmed,
      unit: '+',
      description: '---',
    },
    {
      title: '격리해제',
      number: dashData.today_released,
      unit: '+',
      description:
        '---',
    },
    {
      title: '사망자',
      number: dashData.today_death,
      unit: '+',
      description:
        '---',
    },
  ];


  const countItem1 = {
    0: useScrollCount(dashData.confirmed, dashData.confirmed-200, 0.1),
    1: useScrollCount(dashData.released, dashData.released-200, 0.1),
    2: useScrollCount(dashData.death, dashData.death-200, 0.5),
  };

  const countItem2 = {
    0: useScrollCount(dashData.today_confirmed, 0, 1),
    1: useScrollCount(dashData.today_released, 0, 1),
    2: useScrollCount(dashData.today_death, 0, 0.5),
  };

  const animatedItem = {
    0: useScrollFadeIn('up', 1, 0, 0.5),
    1: useScrollFadeIn('up', 1, 0.1, 0.5),
    2: useScrollFadeIn('up', 1, 0.2, 0.5),
    3: useScrollFadeIn('up', 1, 0.3, 0.5),
  }

  return (
    <S.Background>
      <S.Wrapper>
        <S.Label {...animatedItem[0]}>
          누적 확진자 대시보드 
          <br/>
          {dashData.date} 기준 </S.Label>
        <S.Title {...animatedItem[1]}>
          Total
        </S.Title>
        <S.List>
          {FIGURE_ITEMS.map((item, index) => (
            <S.ListItem key={item.title}>
              <S.Unit>{item.unit}</S.Unit>
              <S.Number {...countItem1[index]}></S.Number>
              <S.Title>{item.title}</S.Title>
              <S.Description>{item.description}</S.Description>
            </S.ListItem>
          ))}
        </S.List>
        <S.Label {...animatedItem[2]}>추가 확진자</S.Label>
        <S.Title {...animatedItem[3]}>
          Today
        </S.Title>
        <S.List>
        {FIGURE_ITEMS2.map((item, index) => (
            <S.ListItem key={item.title}>
              <S.Unit>{item.unit}</S.Unit>
              <S.Number {...countItem2[index]}>0</S.Number> 
              <S.Number></S.Number> 
              <S.Title>{item.title}</S.Title>
              <S.Description>{item.description}</S.Description>
            </S.ListItem>
          ))}
        </S.List>
      </S.Wrapper>
    </S.Background>
  );
};

export default DashBoard;
