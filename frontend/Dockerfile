FROM amazeeio/node:10-latest
RUN npm install --global gatsby-cli
COPY ./map /app
WORKDIR /app
RUN apk update && apk add curl vim
RUN yarn install --pure-lockfile
RUN gatsby build
EXPOSE 3000
EXPOSE 8000
#CMD ["node", "webserver.js"]
#CMD ["sh", "-c", "sleep 2073600"]

CMD ["gatsby", "serve", "-p", "8000", "-H", "0.0.0.0"]
