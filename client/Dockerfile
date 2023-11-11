FROM node:18

LABEL version="1.0"

WORKDIR /xweeter

COPY . .
RUN npm install
RUN npm run build

ENV TZ="Asia/Jakarta"

EXPOSE 4173

CMD ["npm", "run", "preview"]