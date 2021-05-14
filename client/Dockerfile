FROM node:lts-alpine as base
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# development stage
FROM base as development-stage
ENV CONTAINER_PATH /app
EXPOSE 8080
CMD [ "npm", "run", "serve"]

# build stage
FROM base as build-stage
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]