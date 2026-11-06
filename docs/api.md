# API reference

Base URL: `http://localhost:8000` in development. Interactive OpenAPI docs are served at `/docs`.

## Authentication

Sign in with `POST /auth/login` and send the access token on every request:

```http
Authorization: Bearer <access_token>
```

Access tokens last 15 minutes. Exchange the refresh token (30 days) at `POST /auth/refresh` for a new pair. For server-to-server use, create an API key and send it as `X-API-Key: <key>`.

Generation endpoints are rate-limited per user and tier (Free ≈ 2/min, Pro ≈ 10/min). An exceeded limit returns an error whose detail contains `Rate limit exceeded`.

## Endpoints

### Auth

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/login` | — | Passwordless login by email; creates a Free account for new emails. Returns access and refresh tokens. |
| `POST` | `/auth/refresh` | — | Exchange a refresh token for a new token pair |
| `POST` | `/auth/api-keys` | User | Create an API key (the key is shown once) |
| `GET` | `/auth/api-keys` | User | List your API keys |
| `DELETE` | `/auth/api-keys/{key_id}` | User | Revoke an API key |

### Writing

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/idea/generate-idea` | User | `{prompt, genre?, tone?}` → `{title, genre, tone, outline, characters[], setting}` |
| `GET` | `/idea/idea-examples` | — | Example prompts |
| `POST` | `/story/write-story` | User | `{title, genre, outline, tone?, characters?, setting?}` → `{story}` |
| `POST` | `/story/write-story-stream?streaming_speed=slow\|normal\|fast` | User | Same body; streams `data: {json}` events (see below) |
| `POST` | `/story-editor/edit` | User | `{story, edit_instructions, title?, genre?}` → `{success, edited_story, original_story, …}` |
| `GET` | `/story-editor/capabilities` | — | What the editor agent supports |

**Stream events** from `/story/write-story-stream`:

```text
data: {"type": "content", "content": "Every night for eleven years…", "is_final": false}
data: {"type": "metadata", "provider": "gemini", "model": "gemini-2.5-flash", "tokens_in": 0, "tokens_out": 0, "cost_usd": 0}
data: {"type": "complete"}
data: {"type": "error", "error": "…"}
```

### Workflows

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/workflow/generate-full-story` | User | `{prompt, genre?, tone?}` → `{idea, story}` in one call |
| `POST` | `/workflow/generate-idea-only` | User | Idea only, same response shape |
| `GET` | `/workflow/workflow-info` | — | Workflow description |
| `POST` | `/multi-agent/full-story-orchestrated` | User | Idea → story → moderation → QA through the orchestrator |
| `POST` | `/multi-agent/idea-only-orchestrated` | User | Orchestrated idea generation |
| `POST` | `/multi-agent/orchestrated-workflow` | User | Run a custom workflow type |
| `GET` | `/multi-agent/system-status` | User | Agent health and status |
| `GET` | `/multi-agent/workflow-history` | User | Recent workflow executions |

### Account and safety

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/user/me/profile` | User | Profile and plan |
| `GET` | `/user/me/usage` | User | Your usage |
| `GET` | `/moderation/metrics?days=30` | User | Your content-moderation summary |
| `GET` | `/moderation/stats?days=30` | User | Violation breakdown and score ranges |

### Providers

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/providers/providers/available` | User | Configured providers and models |
| `GET` | `/providers/providers/selection-info` | User | How a task and tier map to providers |
| `POST` | `/providers/providers/test` | User | Test a provider connection |
| `GET` | `/providers/providers/health` | User | Provider health |

### Admin (role `admin`)

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/admin/usage/summary` | Usage across all users |
| `GET` | `/admin/usage/leaderboard` | Top users by usage |
| `GET` | `/admin/costs` | Provider cost totals |
| `GET` | `/admin/users` | User list |
| `GET` | `/moderation/admin/metrics` | System-wide moderation metrics |

### Operations

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check |
| `GET` | `/metrics` | Prometheus metrics |
