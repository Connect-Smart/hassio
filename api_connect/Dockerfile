FROM homeassistant/aarch64-addon-base:10.0.0
RUN apk add --no-cache nodejs
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD [ "node", "app.js" ]