---
version: 1
slug: "frontend-src-app-page-tsx"
primary_target: "frontend/src/app/page.tsx"
related_targets: ["frontend/src/app/studio/page.tsx"]
---

## Scope

Whole-system replacement of the visual world for the TaelioAI web frontend. Surfaces: landing `/` (Persuade, signed-out visitors), writing studio `/studio` (Operate, signed-in writers), plus login/register, select-tier and metrics, which inherit the world in Operate register.

Audience: hobbyist writers with a spark. Landing job: understand the spark → idea → story → edit pipeline and start a story. Studio job: move one story through idea, story and edit without retyping, ending with a story worth keeping.

Constraints: no invented stats, testimonials or prices; generation requires login; failures must be explained plainly. Avoid techy/AI-hype and childish registers.

## Direction contract

THESIS: Every story is a numbered paperback in the TaelioAI series. The pipeline is how a book gets made: cover (idea), text (story), revisions (edit). Refuses the AI-SaaS hero (gradient headline, icon cards, stats band) and its cream-and-serif literary opposite.

OWN-WORLD: Three-band paperback covers. Flat genre colour bands own whole regions (series orange #e8641c by default; one colour per genre), with a bright matte white middle band and near-black ink #151515. Display is geometric vintage caps (Josefin Sans); UI is Figtree; story text is Literata. Spines carry series numbers in tabular figures. No gradients, glass or icon tiles.

STORY: A visitor sees that their spark becomes a real book, learns that separate agents make the cover, write the text and revise it, and types a spark straight into the cover to start. A writer sees their book's cover fill in as each stage completes, then keeps the finished paperback.

FIRST VIEWPORT: Landing is one full-bleed three-band cover. The top orange band holds the masthead, series mark and nav. The white middle band holds the headline and a working spark input with genre picker and "Start this story" button. The bottom orange band holds the pipeline line. Studio: orange top bar, left stage stepper, central work area, and on the right a live cover of the book in progress (the signature move).

FORM: Pocket Paperback Series, #1 on my ordered list (IMPECCABLE'S PICK, chosen by the user). seed:ef69286dafc10bd1

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Memorable moment

In the studio, the cover on the right fills in stage by stage: the genre band takes its colour, the title sets on the cover when the idea lands, and the spine gains its word count as the story streams in.

## Unresolved

Free vs pro tier differences and pricing are undecided; the tier page must not invent them.
