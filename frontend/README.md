# TaelioAI web app

The Next.js 14 client for TaelioAI. See the [root README](../README.md) for the product overview and full setup.

## Run it

```bash
npm install
cp .env.example .env.local   # NEXT_PUBLIC_API_URL, defaults to http://localhost:8000
npm run dev                  # http://localhost:3000
```

The API must be running for sign-in and writing to work.

## Scripts

| Command | What it does |
| --- | --- |
| `npm run dev` | Development server with hot reload |
| `npm run build` | Production build (includes lint and type checks) |
| `npm run start` | Serve the production build |
| `npm run type-check` | TypeScript only |

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Landing page: the working cover, how a story gets made, genre shelf |
| `/studio` | The writing studio: Idea → Story → Edit → Book (sign-in required) |
| `/login`, `/register` | Passwordless email sign-in; both accept `?next=` |
| `/select-tier` | Plans |
| `/metrics` | Your content-safety metrics (sign-in required) |

## Code map

```text
src/
├── app/                 # routes (App Router)
├── components/
│   ├── book/BookCover   # the three-band cover used everywhere
│   ├── site/            # header, footer, auth shell, email sign-in
│   └── studio/          # shared studio pieces (errors, headings, downloads)
├── contexts/AuthContext # signed-in user
├── hooks/useApi         # idea, story (streaming) and workflow hooks
└── lib/
    ├── api.ts           # Axios client, token refresh, SSE parsing
    └── series.ts        # genres, band colours, plain-language errors
```

## Design system

Every story is a paperback in the TaelioAI series. Genre colours live in `src/lib/series.ts`; colour, type and radius tokens in `tailwind.config.js`; component classes (`.btn-primary`, `.field`, `.book-text`, …) in `src/app/globals.css`. Fonts: Josefin Sans (display), Figtree (UI), Literata (story text), self-hosted from `src/app/fonts` with `next/font/local` (SIL OFL 1.1).
