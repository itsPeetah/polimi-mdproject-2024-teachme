# Use the official Node.js image as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Ensure local binaries are available in PATH
ENV PATH /app/node_modules/.bin:$PATH

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Debug step to check if node_modules contains Next.js
RUN ls -la node_modules/next

# Copy the rest of the application code to the working directory
COPY . .

# Build the Next.js application
RUN npm run build

# Expose the port that the Next.js app will run on
EXPOSE 3000

# Specify the command to run the application
CMD ["npm", "start"]
