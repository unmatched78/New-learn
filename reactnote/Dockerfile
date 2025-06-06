# frontend/Dockerfile

# 1) Build stage: install dependencies and build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy only package.json and lockfiles first
COPY package.json yarn.lock* package-lock.json* /app/

# Use yarn if a yarn.lock exists; otherwise, do npm install with --legacy-peer-deps
RUN if [ -f yarn.lock ]; then \
      yarn install --frozen-lockfile; \
    else \
      npm install --legacy-peer-deps; \
    fi

COPY . /app/

# Build Vite/React (output to /app/dist)
RUN if [ -f yarn.lock ]; then \
      yarn build; \
    else \
      npm run build; \
    fi

# 2) Serve stage: use NGINX to serve the built files
FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Replace default NGINX config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
# Note: Ensure that the nginx.conf file is properly configured to serve your React app.