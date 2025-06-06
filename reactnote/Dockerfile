# frontend/Dockerfile

# 1. Build stage: install dependencies and build
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* /app/
# Use yarn if yarn.lock exists, otherwise npm
RUN if [ -f yarn.lock ]; then yarn install --frozen-lockfile; else npm install; fi

COPY . /app/

# Run Vite build (outputs to /app/dist by default)
RUN if [ -f yarn.lock ]; then yarn build; else npm run build; fi

# 2. Serve stage: use a lightweight NGINX to serve the built files
FROM nginx:stable-alpine

# Copy the dist folder from the builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Remove default NGINX config and replace with a minimal one
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
# Note: Ensure that the nginx.conf file is properly configured to serve your React app.