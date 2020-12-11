# PlayData-Signature
혁신성장 청년인재 집중양성 데이터과학자 양성과정(2020.06 ~ 2020.12, 960시간)  
멘토링 프로젝트 - 데이터 기반 COVID-19 확진자 및 정보 제공 사이트 구축

## Demo Web-Site Link
아래의 사이트를 접속하시면 확인하실 수 있습니다.  
www.signature-playdata.info


## Docker-compose Setting 
다음 순서대로 동일한 환경의 웹서버를 구축합니다.  
(DB & Cron 서버 설정 제외)  
별도의 MongoDB를 위한 연결은 docker-compose파일의 DBADDR, DBUSER, DBPWD의 변수에 설정합니다.  

---
#### 1. git repository Clone
```
$ git clone 
$ cd PlayData-Signature
$ cd web_server
```

#### 2. Docker-compose up 
```
$ docker-compose up -d --build
```

#### 3. Done!

---
