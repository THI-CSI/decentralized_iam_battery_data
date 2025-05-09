FROM node:23 AS final

WORKDIR /app

RUN <<EOF
set -e
apt-get update
apt-get install -y wget default-jre-headless
EOF

COPY ./frontend . 

RUN chown -R node:node /app

USER node
RUN npm install

CMD ["npm", "run", "dev"]
