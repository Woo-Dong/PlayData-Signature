FROM node:12.18.2

RUN mkdir /app
WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
COPY package.json /app/package.json


RUN npm install 
RUN npm audit fix
RUN npm install react-scripts@3.4.3 -g 

COPY . /app
CMD ["npm", "start"]
