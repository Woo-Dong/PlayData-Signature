import React from 'react';
import styled from 'styled-components';

const S = {
  Background: styled.section`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-top: 120px;
    padding-bottom: 48px;
    height: 100%;
    background: no-repeat center/cover url(${require("../../assets/img/background_simple.png")});
  `,
  Wrapper: styled.div`
    width: 10%;
    height: 100%;
    padding-top: 200px;
    padding-bottom: 200px;
    margin: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    
  `,
  Title: styled.h1`
    ${props => props.theme.typography.title};
    color: #f1c232;
    margin-bottom: 0.5rem;
    
  `,
  Description: styled.p`
    ${props => props.theme.typography.description};
    color: ${props => props.theme.palette.white};
    margin-bottom: 2rem;
  `,
};

const HeaderImg = () => {
  return (
    <S.Background>
      <S.Wrapper>
        <S.Title>
          Signature
          <br />
          Project
        </S.Title>
        <S.Description>
          Information about Corona
          <br />
          
        </S.Description>
      </S.Wrapper>
    </S.Background>
  );
};

export default HeaderImg;