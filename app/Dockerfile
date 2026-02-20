FROM node:23.10.0-alpine AS base

RUN corepack enable

FROM base AS dependencies

RUN apk update && apk add --no-cache gcompat=1.1.0-r4
WORKDIR /app

COPY package.json pnpm-lock.yaml* .npmrc* ./

RUN corepack prepare pnpm@10.30.1 --activate

RUN pnpm install --frozen-lockfile

FROM base AS build
WORKDIR /app

COPY --from=dependencies /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN pnpm build

FROM base AS run
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=build /app/public ./public

COPY --from=build --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=build --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

ENV PORT=$PORT
EXPOSE $PORT

ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]