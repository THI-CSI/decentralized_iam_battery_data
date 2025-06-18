FROM node:23-bookworm-slim AS build-frontend

WORKDIR /app

COPY ./blockchain/frontend/package.json .
COPY ./blockchain/frontend/ .

RUN --mount=type=cache,target=./node_modules/ \
    <<EOF
set -e
npm install
npm clean-install
npm run build
mv ./dist /frontend
EOF

FROM nginx:latest AS final

COPY --from=build-frontend /frontend /usr/share/nginx/html/frontend