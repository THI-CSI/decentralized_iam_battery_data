FROM node:23 AS final

WORKDIR /app

COPY ./frontend . 

RUN chown -R node:node /app

USER node
RUN npm install

CMD ["npm", "run", "dev"]
