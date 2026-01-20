# 1. Use the official Node.js image (Lightweight version)
FROM node:18-alpine

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy package.json and package-lock.json FIRST
# This allows Docker to cache dependencies if they haven't changed.
COPY package*.json ./

# 4. Install dependencies inside the container
RUN npm install

# 5. Copy the rest of your code
COPY . .

# 6. Expose the port Vite runs on (usually 5173)
EXPOSE 5173

# 7. Start the app ensuring it accepts external connections
# --host 0.0.0.0 is CRITICAL for Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]