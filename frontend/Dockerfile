FROM amazeeio/node:10-latest
RUN npm install --global gatsby-cli
COPY ./map /app
WORKDIR /app
RUN apk update && apk add curl vim
RUN yarn install --pure-lockfile
#RUN gatsby build
EXPOSE 3000
EXPOSE 8000
CMD ["gatsby", "serve", "-p", "8000", "-H", "0.0.0.0"]
