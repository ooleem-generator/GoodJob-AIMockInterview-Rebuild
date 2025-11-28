# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack application with separate frontend and backend directories:

- **Frontend**: Next.js 16 (App Router) with React 19, TypeScript, and Tailwind CSS v4
- **Backend**: Python FastAPI with uvicorn server

## Development Commands

### Frontend (`/frontend`)

```bash
# Install dependencies
npm install

# Run development server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### Backend (`/backend`)

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux

# Install dependencies (using uv)
uv sync

# Run FastAPI server
uvicorn app:app --reload

# Run main script
python main.py
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
