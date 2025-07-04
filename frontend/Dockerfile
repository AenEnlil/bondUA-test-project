FROM node:22.15.0-alpine as build-stage

WORKDIR /app
COPY . .

ARG VITE_BACKEND_API_URL
ENV VITE_BACKEND_API_URL=$VITE_BACKEND_API_URL

RUN npm install
RUN npm run build

FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]