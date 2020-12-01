import React from 'react'; 
import styled from 'styled-components';
import introduceImg1 from '../assets/img/dw.gif';
import introduceImg2 from '../assets/img/jh.jpg'; 
import introduceImg3 from '../assets/img/sh.jpg'; 

import { useScrollFadeIn } from '../hooks'; 

const S = {
  Wrapper: styled.div`
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
    color: #f1c232;
    text-align: center;
    margin-bottom: 1rem;
  `,
  Description: styled.p`
    ${props => props.theme.typography.description};
    color: ${props => props.theme.palette.black};
    margin-bottom: 4rem;
  `,
  List: styled.ul`
    width: 100%;
    display: flex;
    flex-direction: row;
    padding-right: 40px;
    margin-bottom: 4rem;
  `,
  ListItem: styled.li`
		width: 500px;
    box-shadow: 0 0 16px 8px rgba(0, 0, 0, 0.03);
		border-radius: 0.5rem;
		&:nth-child(2) {
      border: 8px solid ${(props) => props.theme.palette.white};
      border-top: none;
      border-bottom: none;
    }
  `,
  ItemImage: styled.div`
    width: 100%;
    height: 380px;
    border-radius: 1.5rem 1.5rem 0 0;
    background: no-repeat center/cover url(${props => props.image});
  `,
  TextContainer: styled.div`
    padding: 4rem;
  `,
  ItemTitle: styled.h3`
    ${props => props.theme.typography.heading};
    color: ${props => props.theme.palette.black};
    margin-bottom: 0.75rem;
  `,
  ItemLabel: styled.p`
    ${props => props.theme.typography.caption};
    color: ${props => props.theme.palette.gray};
    font-weight: 400;
    margin-bottom: 1.5rem;
  `,
  ItemDesciption: styled.p`
    ${props => props.theme.typography.description};
  `,
  TextButton: styled.button`
    width: fit-content;
    padding: 0;
    ${props => props.theme.typography.textbutton};
    color: ${props => props.theme.palette.secondary};
    cursor: pointer;
  `,
};

const WORKS_ITEMS = [
  {
		image: introduceImg1,
    title: '박동우',
    label: '#Full_Stack #Dev-Analyst #즐기면서_실용적인',
    description:
      '후룰룰루 훈화말씀',
	},
	
  {
    image: introduceImg2,
    title: '백지훈',
    label: '#kpop #k방역 #bts #불닭볶음면 #kstartup',
    description:
      '경제적 자유를 추구하는 백지훈입니다. 주식, 스타트업에 관심이 많습니다.',
	},
	{
    image: introduceImg3,
    title: '강셰인',
    label: '#호주 #달리기 #강릉 #108배 #몽중인백짬뽕',
    description:
      '디지털 노마드 여정을 시작한 강셰인입니다. 여행과 수행이 취미입니다.',
  },
];

const Info = () => {

	const animatedItem = { 
		0: useScrollFadeIn('left',     1,   0, 0.5),
    1: useScrollFadeIn('left',     1, 0.3, 0.5),
    2: useScrollFadeIn('left', 	 0.5, 0.6, 0.5),
	}

  return (
    <S.Wrapper>
      <S.Label>만든이 소개</S.Label>
      <S.Title>
				<b>Signature Team</b>
      </S.Title>
      <S.Description>
				- PlayData 프로젝트 -
      </S.Description>
      <S.List>
        {WORKS_ITEMS.map((item, index) => (
          <S.ListItem key={item.title} {...animatedItem[index]}>
            <S.ItemImage image={item.image} />
            <S.TextContainer>
              <S.ItemTitle>{item.title}</S.ItemTitle>
              <S.ItemLabel>{item.label}</S.ItemLabel>
              <S.ItemDesciption>{item.description}</S.ItemDesciption>
							<br />
              <S.TextButton>Git Hub Link</S.TextButton>
            </S.TextContainer>
          </S.ListItem>
        ))}
      </S.List>
    </S.Wrapper>
  );
};
export default Info; 

