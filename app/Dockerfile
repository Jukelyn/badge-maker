FROM node:23.10.0-alpine AS base
WORKDIR /app

RUN apk update && apk add --no-cache libc6-compat=1.2.3-r0

# === Install deps ===
FROM base AS deps
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./
RUN npm install -g npm@11.2.0 && npm ci

# === Build the app ===
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# === Final runtime ===
FROM base AS runner

# Create non-root user
RUN addgroup -S nodejs && adduser -S nextjs -G nodejs

WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget -q --spider http://badge_maker_api:5000/health || exit 1

USER nextjs

EXPOSE 3000
CMD ["npm", "start"]
