FROM node:16-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install

# add app
COPY . .

EXPOSE 8080

# start app
CMD ["npm", "run", "serve"]
