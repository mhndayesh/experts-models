# Web Expert — coverage (built 2026-07-16)

The **Web** department bank (merge of frontend + backend per the DEPARTMENTS.md owner call). Built
end-to-end with the proven pipeline: **FIND migration guide → WebFetch source → DeepSeek extract →
repair → check**. All facts quote-grounded; integrity verified (0 duplicate ids within/cross-bank,
100% truth+quote, 0 bad types).

## Banks
| library | version | facts | source (migration guide) |
|---|---|---|---|
| tailwind | v4 | 56 | tailwindcss.com/docs/upgrade-guide |
| pydantic | v2 | 54 | pydantic.dev migration guide |
| react | 19 | 29 | react.dev React 19 upgrade guide |
| svelte | 5 (runes) | 29 | svelte.dev v5 migration guide |
| vue | 3 | 29 | v3-migration.vuejs.org |
| sqlalchemy | 2.0 | 24 | docs.sqlalchemy.org migration_20 |
| django | 5 | 16 | docs.djangoproject.com release/deprecation notes |
| express | 5 | 27 | expressjs.com 5.x migration guide |
| nextjs | 15 | 15 | nextjs.org upgrade/codemod guide |
| **total** | | **279** | 9 banks |

Sources saved under `sources/`, banks under `facts/`.

## Why these (landmine density)
Frontend/backend web is the **most habit-reversal-dense** domain — the fastest-moving stack where a
model's training is most stale. Every bank is dominated by REPLACED/REMOVED facts (renames, removed
APIs, changed defaults), which is exactly the fact type the bank exists to carry and the type reasoning
tends to revert on (see `../../../eval/gitchameleon/QWEN-THINKING-AUTHORITY.md`). Examples that bite:
- pydantic `.dict()`→`.model_dump()`, `__fields__`→`model_fields`, `@validator`→`@field_validator`
- react `ReactDOM.render`→`createRoot`, removed `defaultProps`/`propTypes`/string refs
- svelte `let`→`$state`, `$:`→`$derived`/`$effect`, `on:click`→`onclick`, slots→snippets
- tailwind `@tailwind`→`@import`, `shadow-sm`→`shadow-xs`, `ring` now 1px, border color→`currentColor`
- vue `new Vue()`→`createApp()`, filters removed, `$children`/`$listeners` removed
- sqlalchemy `engine.execute()`→`connect()`, `Query`→`select()`, `session.query().get()`→`session.get()`

## Not yet built (next)
- **Bake + score** this department into a GGUF and run a web eval (no web benchmark run yet — GitChameleon
  is Python-scientific; a web-specific eval set is needed to score these).
- More web libs with clean migration guides: FastAPI, Angular, Nuxt, Prisma/Drizzle.

The **Security & Networking** department is built, baked, and tested (114 facts, 7 libraries, 26b) — see
`../security-networking/README.md`. See `../DEPARTMENTS.md` for the full catalog and roadmap.
