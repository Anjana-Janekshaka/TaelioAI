# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Hobbyist writers: people who write stories for fun, often without a regular practice or formal training. They arrive with a spark (a character, a premise, a single image) and want help turning it into a finished short story they can read, tweak and share. Sessions are casual and self-directed, usually on a laptop.

## Product Purpose

TaelioAI is an AI storytelling companion. It takes a writer from a loose prompt to a story idea (title, genre, tone, outline, characters, setting), then to a drafted story, then through instruction-driven edits. Success means a hobbyist leaves with a story that feels like theirs and that they would not have finished alone.

## Positioning

A pipeline of specialised agents, not a single chat prompt. Separate agents handle idea generation, story writing, content moderation, quality assurance and editing, and the product walks the writer through that spark → idea → story → edit sequence step by step. Each stage's output becomes the next stage's input.

## Operating Context

- Flow: generate an idea from a prompt plus optional genre and tone → write a story from title, genre, tone, outline, characters and setting (streamed in as it is written, at slow, normal or fast speed) → edit the story with free-text instructions.
- Passwordless login by email; users have a tier (free or pro), and a tier-selection page exists.
- A moderation metrics page reports the user's content-safety data (items moderated, violations, safety-score distribution) over a selectable period.

## Capabilities and Constraints

- Frontend: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Framer Motion, lucide-react icons, in `frontend/`.
- Backend: FastAPI at `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`); story generation uses Gemini, and other providers are configured.
- Tiers that exist in the backend: Free (about 2 generation requests per minute) and Pro (about 10 per minute). There is no Premium tier, no payment system and no price; Pro is presented as coming soon, with no price.
- Generation can fail, be rate-limited or be slow; the UI must handle that.
- All generation endpoints require login. Sign-in is passwordless by email only; there is no social or OAuth sign-in.
- Genres offered: Fantasy, Science Fiction, Mystery, Romance, Horror, Thriller, Adventure, Drama. Tones offered: Adventurous, Dark, Light-hearted, Mysterious, Romantic, Gritty, Whimsical, Dramatic.
- Undecided: pricing for Pro.

## Brand Commitments

- Name: TaelioAI. Tagline in use: "Your AI Storytelling Companion".
- No logo or other brand assets exist in the repo.

## Evidence on Hand

- No real usage numbers, testimonials, customers or press. The earlier home-page stats ("10,000+ Stories Generated", "5,000+ Happy Writers", "99.9% Success Rate") were placeholders and must not be shown or replaced with invented figures.
- Factual: the system has five agents (idea generator, story writer, content moderator, quality assurance, story editor).

## Product Principles

1. The writer's spark leads. Prompts, choices and edit instructions steer every agent, and the UI keeps the writer's input visible next to the output.
2. Show the pipeline. Make the stages and the hand-off between them legible, because the staged pipeline is what separates TaelioAI from a single chat box.
3. Welcoming, not technical. Hobbyists should never need to understand models, providers or tokens to finish a story.
4. Finish the story. Every screen should move the writer toward a complete, readable story they can keep.
5. Honest by default. No invented social proof; failures and limits are explained plainly.
