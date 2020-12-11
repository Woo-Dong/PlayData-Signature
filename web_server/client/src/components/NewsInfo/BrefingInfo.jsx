import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Axios from 'axios'; 
import { useScrollFadeIn } from '../../hooks';

const S = {
  Wrapper: styled.section`
    width: 100%;
    max-width: 1180px;
    margin: auto;
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
    text-align: center;
  `,
  ItemWrapper: styled.ul`
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding-right: 40px;
  `,
  ItemBox: styled.li`
    width: 100%;
    text-align: center;
    background-color: ${props => props.theme.palette.white};
    display: flex;
    flex-direction: column;
    box-shadow: 0 0 16px 8px rgba(0, 0, 0, 0.03);
    border-radius: 0.5rem;
  `,
  ItemTitle: styled.h3`
    ${props => props.theme.typography.heading};
    color: ${props => props.theme.palette.black};
    margin-bottom: 1rem;
  `,
  ItemDescription: styled.p`
    ${props => props.theme.typography.description};
    margin-bottom: 1.5rem;
  `,
  ItemButton: styled.button`
    ${props => props.theme.typography.textbutton};
    color: ${props => props.theme.palette.secondary};
    margin-top: auto;
    cursor: pointer;
  `,
};



const BrefingInfo = () => {


  const brefingDataState = { 
    title: "",
    date: "",
    contents: []
  }; 

  const [brefingData, setBrefingData] = useState(brefingDataState); 

  useEffect(() => {
    Axios.get("/api/brefing-info")
      .then(response => {
        setBrefingData({
          title: response.data.title, 
          date: response.data.date,
          contents: response.data.contents
        })
    })
  }, []);

  const SERVICES_ITEMS = [
    {
      title: 
        "1번째 문단",
      description:
        brefingData.contents[0],
      // button: 'et started',
    }, 
    {
      title: 
        "2번째 문단",
      description:
        brefingData.contents[1],
    }, 
    {
      title: 
        "3번째 문단",
      description:
        brefingData.contents[2],
    }
  ];

  const animatedItem = {
    0: useScrollFadeIn('up', 1, 0),
    1: useScrollFadeIn('up', 1, 0.2),
    2: useScrollFadeIn('up', 1, 0.3),
  };

  return (
    <S.Wrapper>
      <S.Label>정부 브리핑 최신 내용 요약</S.Label>
      <S.Title>{brefingData.title}</S.Title>
      <S.ItemTitle>게시 날짜: {brefingData.date}</S.ItemTitle>
      {SERVICES_ITEMS.map((item, index) => (
        <S.ItemWrapper key={item.title} {...animatedItem[index]}>
          <S.ItemBox>
            <S.ItemTitle>{item.title}</S.ItemTitle>
            <S.ItemDescription>{item.description}</S.ItemDescription>
          </S.ItemBox>
        </S.ItemWrapper>
      ))}
    </S.Wrapper>
  );
};

export default BrefingInfo;
