# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Job application tracker. Python 3.11+, SQLAlchemy 2.0 (declarative, typed `Mapped[...]` columns) on Postgres, managed with Poetry, migrations via Alembic. There is no application/API layer yet — only the data model, DB config, and migration setup exist so far.

## Commands

Dependencies and the virtualenv are managed by Poetry (`.venv` is in-project — see `.vscode/settings.json`). Run project commands through Poetry so they use that venv:

```bash
poetry install                          # install/sync dependencies
poetry run alembic revision --autogenerate -m "message"   # generate a migration from model changes
poetry run alembic upgrade head         # apply migrations
poetry run alembic downgrade -1         # revert one migration
poetry run python -c "..."              # run a one-off script in the project venv
poetry run mypy src/                    # type-check the src package
```

Local Postgres runs via Docker Compose (`docker-compose.yml`, mapped to `localhost:5432`):

```bash
docker-compose up -d
```

mypy is configured in `[tool.mypy]` in `pyproject.toml` (`strict = true`) as a `dev` dependency group. The `relationship()` type hints in `src/models/` use string forward references (e.g. `Mapped["Application"]`) that SQLAlchemy resolves at runtime via its mapper registry, but mypy needs the referenced class importable in-module — each model file guards these imports behind `if TYPE_CHECKING:` to satisfy mypy without introducing circular imports at runtime. No test suite or formatter is configured yet.

## Architecture

- **`src/` is the actual top-level Python package** (not `job_tracker`) — all internal imports use `from src.models... import ...`, `from src.config import settings`. This is intentional; `pyproject.toml` has both `[tool.poetry] packages = [{ include = "src" }]` and `[tool.setuptools.packages.find]` configured to discover `src` itself as the installable package. Poetry's own package-discovery (used when installing the root project) ignores the setuptools `packages.find` config entirely, so both must stay in sync — if the package layout ever changes, update both.
- **Config (`src/config.py`)**: a single `pydantic-settings` `Settings` class loaded from `.env`. Database credentials are individual fields (`postgres_user`, `postgres_password`, `postgres_db`, `postgres_host`, `postgres_port`), and `database_url` is a computed `@property` that assembles the `postgresql+psycopg://` URL from them — it is **not** read as a single `DATABASE_URL` env var with nested `${VAR}` interpolation. That approach was deliberately abandoned: pydantic-settings/python-dotenv's handling of nested `${VAR}` references inside `.env` proved inconsistent across shells/processes (silently leaving literal `${POSTGRES_USER}` unexpanded in some cases, causing Postgres auth failures). Don't reintroduce a single interpolated `DATABASE_URL` env var — add new connection parameters as their own typed fields instead.
- **Models (`src/models/`)**: one SQLAlchemy model per file, all inheriting from `Base` (`src/models/base.py`, a plain `DeclarativeBase`). `src/models/__init__.py` re-exports everything and is the single import point (`from src.models import Base, User, Application, ...`); add new models there too so Alembic autogenerate and `env.py` see them via `Base.metadata`.
- **Schema relationships**: `User` (one) → `Application` (many, `user_id` FK) → `Interview`, `Contact`, `StatusEvent` (each many-to-one via an `application_id` FK). All PKs are `uuid.UUID` generated client-side via `uuid.uuid4`. Every FK pair has a matching ORM `relationship()`/`back_populates` on both sides (e.g. `Application.contacts` ↔ `Contact.application`), not just raw FK columns — when adding a new FK, add the relationship pair too. `cascade="all, delete-orphan"` belongs on the "one"/collection side (e.g. `Application.interviews`), never on the "many"/scalar side (e.g. `Interview.application`) — putting it on the wrong side is a common mistake here since `back_populates` alone won't catch it at import time.
- **DB session (`src/database.py`)**: `engine`/`SessionLocal` built from `settings.database_url` — the entrypoint any future API/service code should import for DB access, rather than constructing its own engine.
- **Alembic wiring (`alembic/env.py`)**: imports `settings` and `Base` directly from `src`, sets `sqlalchemy.url` at runtime from `settings.database_url` (via `config.set_main_option`), and sets `target_metadata = Base.metadata` for autogenerate. `alembic.ini`'s `sqlalchemy.url` line is intentionally commented out/unused — the real URL always comes from `src.config.settings`. Autogenerate only detects schema-level diffs (columns, constraints, tables) — adding/changing `relationship()`s alone produces an empty migration, since those are ORM-only constructs; don't bother committing a no-op migration if that's all that changed.
