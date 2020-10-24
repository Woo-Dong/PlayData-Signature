import React from 'react';
import styled from 'styled-components';

const S = {
  Background: styled.section`
    position: absolute;
    top: 0;
    width: 100%;
    height: 780px;
    background: no-repeat center/cover url(${require("../assets/img/background_simple.png")});
  `,
  Wrapper: styled.div`
    width: 100%;
    height: 100%;
    max-width: 1180px;
    padding-top: 100px;
    margin: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
  `,

  Title: styled.h1`
    ${props => props.theme.typography.title};
    color: #fff;
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