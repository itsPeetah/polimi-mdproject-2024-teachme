FROM node:18-alpine

# Set up environment variables for TeachMe Frontend
ENV NEXT_PUBLIC_SPEECH_KEY=${AZURE_KEY}
ENV NEXT_PUBLIC_SPEECH_REGION='westeurope'

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_ENV production

# install and cache app dependencies
COPY . .

RUN npm install
# RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev"]