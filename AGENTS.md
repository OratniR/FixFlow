# FixFlow Developer Guide & Agent Rules

This document outlines the development standards, commands, and architectural patterns for the FixFlow repository. All human and AI contributors must adhere to these guidelines.

## 📂 Project Structure

- **root**: Monorepo root.
- **backend/**: FastAPI (Python 3.11+) application.
- **frontend/**: Next.js 14 (TypeScript) application.

## 🐍 Backend (Python/FastAPI)

### Commands
Run these from `backend/` directory:

- **Run Dev Server**: `uvicorn app.main:app --reload`
- **Run Tests**: `pytest`
- **Run Single Test**: `pytest tests/path/to/test_file.py::test_function_name`
- **Lint**: `ruff check .`
- **Format**: `black .`
- **Type Check**: `mypy .`

### Code Style & Guidelines
- **Type Hints**: **MANDATORY** and **STRICT**. All functions must have argument and return type annotations.
  - `mypy` is configured with `disallow_untyped_defs = true`.
- **Framework**: FastAPI. Use Pydantic v2 models for data validation.
- **Async**: Use `async def` for all route handlers and I/O bound operations.
- **Formatting**:
  - Line length: 100 characters.
  - Follow `black` and `ruff` rules.
- **Naming**:
  - Functions/Variables: `snake_case`
  - Classes: `PascalCase`
- **Imports**: Sorted by `ruff` (isort rules).

## ⚛️ Frontend (Next.js/TypeScript)

### Commands
Run these from `frontend/` directory:

- **Run Dev Server**: `npm run dev`
- **Run Tests**: `npm test` (Jest)
- **Run Single Test**: `npm test -- -t "test name pattern"`
- **Lint**: `npm run lint`
- **Type Check**: `npm run type-check` (tsc --noEmit)
- **Format**: `npm run format`

### Code Style & Guidelines
- **Framework**: Next.js 14 with App Router (`src/app`).
- **Language**: TypeScript (Strict Mode).
  - Avoid `any`. Use specific types or Generics.
  - Interfaces over Types for object definitions.
- **Components**:
  - Use **Function Declarations**: `export default function ComponentName() { ... }`
  - Place in `src/components/`.
- **Styling**: **Tailwind CSS**.
  - Use utility classes directly in `className`.
  - No CSS-in-JS libraries unless explicitly approved.
- **State Management**:
  - React Hooks (`useState`, `useReducer`) for local state.
  - Context API for simple global state.
- **Imports**:
  - Use absolute imports with `@/` alias (points to `src/`).
  - Example: `import Button from '@/components/Button'`

## 🛠️ General Workflow

1.  **Monorepo Operation**: Always check which directory you are in (`backend` vs `frontend`) before running commands.
2.  **Coding Philosophy**:
    - **Abstract to Concrete**: Write code top-down. Start with high-level logic that reads like an English sentence (the "story"), using stubs or interfaces for the details.
    - **Stub to Driver**: Define the "what" (interface/stub) before the "how" (implementation).
3.  **Testing**:
    - Write tests for new features.
    - Run existing tests to ensure no regressions.
3.  **Error Handling**:
    - Backend: Use HTTP exceptions (`raise HTTPException(status_code=404, detail="...")`).
    - Frontend: Use Error Boundaries and `try/catch` blocks for async operations.

## 🤖 AI Agent Instructions

- **Context First**: Before editing, always read related files to understand existing patterns.
- **Minimal Changes**: Do not refactor unrelated code unless necessary.
- **Verify**: After changes, run type checks (`mypy` or `tsc`) and linters to ensure compliance.
- **Documentation**: Update docstrings (Python) or JSDoc (TS) if logic changes significantly.

## 🧠 Knowledge Preservation Protocol

**If you encounter a complex issue (requires 2+ attempts to fix or deep reasoning):**
1.  **Solve it**: Apply the fix and verify it works.
2.  **Store it**: IMMEDIATELY use the `fixflow_knowledge_base` tool (action: `store`) to save the Problem and Solution.
    *   **Query**: The error message or specific challenge.
    *   **Solution**: The working fix, including context on *why* it failed initially.
3.  **Search First**: Before solving a hard problem, check if a solution already exists using `fixflow_knowledge_base` (action: `search`).
