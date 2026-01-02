# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack application with separate frontend and backend directories:

- **Frontend**: Next.js 16 (App Router) with React 19, TypeScript, Tailwind CSS v4, and pnpm
- **Backend**: Python FastAPI with uvicorn server

### Project Goal

This project aims to **rebuild and deploy the AI Mock Interview feature** as a standalone service, separated from the original Good Job recruitment platform.

**Original Project Location**: `/Users/tantalope/Dropbox/KRAFTON JUNGLE/GoodJob`

### Key Differences from Original

| Aspect          | Original Project  | New Project (Rebuild)    |
| --------------- | ----------------- | ------------------------ |
| Package Manager | pnpm              | **pnpm** ✅              |
| Tailwind CSS    | v3                | **v4** (with PostCSS)    |
| UI Components   | Ant Design        | **shadcn/ui** (Radix UI) |
| Authentication  | Custom OAuth      | **Clerk**                |
| Backend         | NestJS + FastAPI  | **FastAPI only**         |
| Main Feature    | Multiple features | **AI Interview only**    |

## Development Commands

### Frontend (`/frontend`)

**IMPORTANT**: This project uses **pnpm** as the package manager.

```bash
# Install dependencies
pnpm install

# Run development server (http://localhost:3000)
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run linter
pnpm lint

# Add shadcn/ui components
pnpm dlx shadcn@latest add [component-name]
```

### Backend (`/backend`)

**IMPORTANT**: Backend uses **Supabase** for database and storage.

#### Initial Setup

```bash
# 1. Activate virtual environment
source .venv/bin/activate  # macOS/Linux

# 2. Install dependencies (using uv)
uv sync

# 3. Start local Supabase (requires Docker - first time only)
supabase start
```

#### Daily Development Workflow

```bash
# 1. Start local Supabase (if not already running)
supabase start

# 2. Run FastAPI server (automatically loads .env.local)
uvicorn app:app --reload

# Alternative: Explicitly specify environment file
ENV_FILE=.env.local uvicorn app:app --reload
```

#### Production Deployment

```bash
# Run with production environment
ENV_FILE=.env.production uvicorn app:app

# Or set environment variable
export ENV_FILE=.env.production
uvicorn app:app
```

#### Supabase Local Development

```bash
# Start local Supabase (requires Docker)
supabase start

# Stop local Supabase
supabase stop

# View local Supabase Studio (Database UI)
# Opens at: http://127.0.0.1:54323

# Reset local database (WARNING: deletes all data)
supabase db reset

# Generate database types (TypeScript)
supabase gen types typescript --local > types/supabase.ts

# Create a new migration
supabase migration new <migration_name>

# Apply migrations to local database
supabase db reset  # or supabase migration up
```

#### Supabase Production

```bash
# Pull schema from production
supabase db pull

# Push migrations to production
supabase db push

# View remote database diff
supabase db diff -f <migration_name>
```

## Architecture

### Frontend Structure

- **App Router**: Uses Next.js App Router pattern (not Pages Router)
- **Path Aliases**: `@/*` maps to the root directory (configured in tsconfig.json)
- **Styling**: Tailwind CSS v4 with PostCSS
- **TypeScript**: Strict mode enabled, targeting ES2017

### Backend Structure

- **Framework**: FastAPI with async support
- **Python Version**: Requires Python >=3.12
- **Package Management**: Uses `uv` for dependency management (pyproject.toml + uv.lock)
- **Virtual Environment**: `.venv` directory (should not be committed)
- **Database**: Supabase (PostgreSQL + Storage + Auth)
  - Local development: Uses Supabase CLI with Docker
  - Production: Connects to Supabase Cloud

### Environment Variables

The backend uses **three separate .env files**:

- **`.env`**: Supabase CLI access token only (for `supabase db pull/push`)
- **`.env.local`**: Local development with Supabase CLI (localhost URLs) - **Default**
- **`.env.production`**: Production deployment (Supabase Cloud URLs)

**How it works:**
- `src/config.py` uses the `ENV_FILE` environment variable to determine which file to load
- If `ENV_FILE` is not set, it defaults to `.env.local` for local development
- To use production settings, set `ENV_FILE=.env.production` before running the server

**Local Supabase URLs** (after running `supabase start`):
- API: `http://127.0.0.1:54321`
- Database: `postgresql://postgres:postgres@127.0.0.1:54322/postgres`
- Studio (UI): `http://127.0.0.1:54323`
- Auth: `http://127.0.0.1:54321/auth/v1`

## Key Configurations

### Frontend

- TypeScript path mapping: `@/*` imports resolve from project root
- ESLint configured with Next.js recommended rules
- React JSX runtime (no React import needed in components)

### Backend

- FastAPI app instance defined in `app.py`
- Currently minimal setup (incomplete route in app.py)
- Dependencies managed via pyproject.toml

## Notes

- This is a monorepo with a single git repository at the root level
- Frontend and backend are separate directories within the monorepo
- No monorepo tooling currently configured (no workspace configuration)
- Backend appears to be in early setup stage (minimal code)
