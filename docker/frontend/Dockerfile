FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

# ---- dev ----
FROM base AS dev
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ---- build ----
FROM base AS build
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# ---- prod ----
FROM nginx:alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html