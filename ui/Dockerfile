FROM node:18-alpine

# Set up environment variables for TeachMe Frontend
# ENV NEXT_PUBLIC_SPEECH_KEY=<YOUR_TTS_AZURE_KEY>
# ENV NEXT_PUBLIC_SPEECH_REGION='westeurope'

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY . .

RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]