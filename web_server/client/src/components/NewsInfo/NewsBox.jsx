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
    margin-bottom: 4rem;
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



const NewsBox = () => {


  const contentDataState = { 
    content: []
  }; 

  const [contentData, setContentData] = useState(contentDataState); 

  useEffect(() => {
    Axios.get("/api/news-summary")
      .then(response => {
        setContentData({
          content: response.data.contents
        })
    })
  }, []);


  const SERVICES_ITEMS = [
    {
      title: '1번째 뉴스 요약',
      description:
        contentData.content[0],
      // button: 'Get started',
    },
    {
      title: '2번째 뉴스 요약',
      description:
      contentData.content[1],
    },
    {
      title: '3번째 뉴스 요약',
      description:
      contentData.content[2],
    },
    // {
    //   title: '4번째 뉴스 요약',
    //   description:
    //   contentData.content[3],
    // },
    // {
    //   title: '5번째 뉴스 요약',
    //   description:
    //   contentData.content[4],
    // }
  ];

  const animatedItem = {
    0: useScrollFadeIn('up', 1, 0),
    1: useScrollFadeIn('up', 1, 0.2),
    2: useScrollFadeIn('up', 1, 0.3),
    3: useScrollFadeIn('up', 1, 0.4),
    4: useScrollFadeIn('up', 1, 0.5),

  };

  return (
    <S.Wrapper>
      <S.Label>최신 뉴스 요약</S.Label>
      <S.Title>
        최근 코로나 및 확진자 관련
        <br />
        뉴스 요약 내용
      </S.Title>
      {SERVICES_ITEMS.map((item, index) => (
        <S.ItemWrapper key={item.title} {...animatedItem[index]}>
          <S.ItemBox>
            <S.ItemTitle>{item.title}</S.ItemTitle>
            <S.ItemDescription>{item.description}</S.ItemDescription>
            {/* <S.ItemButton>{item.button}</S.ItemButton> */}
          </S.ItemBox>
        </S.ItemWrapper>
      ))}
    </S.Wrapper>
  );
};

export default NewsBox;
