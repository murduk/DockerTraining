FROM node:bullseye as build
COPY . .
RUN npm install
RUN npm run build

FROM nginx:1.17.1-alpine
COPY --from=build build /usr/share/nginx/html
