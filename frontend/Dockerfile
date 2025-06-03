# syntax=docker/dockerfile:1

ARG NODE_VERSION=22
ARG NGINX_VERSION=1.27

################################################################################
FROM node:${NODE_VERSION}-alpine AS build

ENV NODE_ENV=production

WORKDIR /app

RUN corepack enable pnpm

ADD . /app

RUN --mount=type=cache,target=/root/.pnpm \
    pnpm install 

RUN --mount=type=bind,source=.env,target=.env \
    pnpm build

################################################################################
FROM nginx:${NGINX_VERSION}-alpine

COPY --from=build /app/dist /opt/public

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl -f http://127.0.0.1 || exit 1
