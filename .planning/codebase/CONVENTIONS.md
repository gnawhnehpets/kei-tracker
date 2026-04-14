# Coding Conventions

**Analysis Date:** 2026-04-14

## Naming Patterns

**Files:**
- **Python:** `snake_case.py` (e.g., `api/main.py`, `data-sync/main.py`)
- **TypeScript:** `camelCase.ts` for hooks (e.g., `frontend/src/hooks/useShipHistory.ts`), `kebab-case.ts` for general files (e.g., `frontend/src/api/client.ts`).

**Functions:**
- **Python:** `snake_case` (e.g., `serialize_doc`, `get_ship_history`, `collect_sample_mmsis`)
- **TypeScript:** `camelCase` (e.g., `useShipHistory`, `fetchShips`)

**Variables:**
- **Python:** `snake_case` (e.g., `client`, `mmsi`, `message_type`)
- **TypeScript:** `camelCase` (e.g., `mmsi`, `since`, `params`), `ALL_CAPS` for constants (e.g., `BASE`)

**Types:**
- **Python:** `PascalCase` for imported types (e.g., `FastAPI`, `HTTPException`). Custom data structures often handled via dictionaries or Pydantic `BaseModel`.
- **TypeScript:** `PascalCase` for interfaces (e.g., `Ship`, `PositionRecord`)

## Code Style

**Formatting:**
- **Python:** 4-space indentation observed. No explicit formatter config detected (e.g., Black).
- **TypeScript:** 2-space indentation observed. No explicit formatter config detected (e.g., Prettier, Biome).

**Linting:**
- No explicit linting tools or configurations detected for either Python (e.g., Flake8, MyPy) or TypeScript (e.g., ESLint).

## Import Organization

**Order:**
- **Python:** Standard library imports, followed by third-party libraries, then local modules.
- **TypeScript:** Node module imports, followed by relative local module imports.

**Path Aliases:**
- Not detected. Relative paths used for local imports.

## Error Handling

**Patterns:**
- **Python:**
    - FastAPI `HTTPException` used for API validation and not found errors.
    - `try...except` blocks used for `ValueError` (e.g., date parsing) and database operation errors.
- **TypeScript:**
    - `if (!res.ok) throw new Error(...)` pattern for API call failures.

## Logging

**Framework:**
- **Python:** `print` statements used for basic console logging in `data-sync/main.py`.
- **TypeScript:** Not explicitly observed, likely relies on browser console for errors.

**Patterns:**
- **Python:** Log messages include timestamps for connection and database events.

## Comments

**When to Comment:**
- **Python:** Docstrings used for FastAPI endpoint descriptions and some function explanations.
- **TypeScript:** Not extensively used in the observed files, mostly self-documenting.

**JSDoc/TSDoc:**
- Not detected.

## Function Design

**Size:**
- Functions generally focused on a single responsibility.

**Parameters:**
- Explicitly typed in Python (type hints) and TypeScript.
- Optional parameters indicated with `Optional` in Python and `?` in TypeScript.

**Return Values:**
- Explicitly typed in Python (type hints) and TypeScript.

## Module Design

**Exports:**
- **Python:** Functions are directly defined and used or implicitly exposed in `main` scripts.
- **TypeScript:** `export` keyword used for functions and interfaces.

**Barrel Files:**
- Not detected.

---

*Convention analysis: 2026-04-14*