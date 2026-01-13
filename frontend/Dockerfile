# Use Node.js LTS (20)
FROM node:20-slim

WORKDIR /app

# Install dependencies first (caching)
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

# Expose Next.js port
EXPOSE 3000

# Start in dev mode for hot reloading
CMD ["npm", "run", "dev"]
