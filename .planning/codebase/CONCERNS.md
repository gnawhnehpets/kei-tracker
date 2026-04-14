# Codebase Concerns

**Analysis Date:** 2026-04-14

## Tech Debt

**ShipHistory Component Complexity:**
- Issue: The `ShipHistory.tsx` component is overly large and complex, handling multiple responsibilities including data fetching, map initialization and manipulation (drawing tracks, updating markers), state management, and UI rendering logic (header, range selector, map, charts).
- Files: `frontend/src/pages/ShipHistory.tsx`
- Impact: This leads to reduced reusability, increased difficulty in understanding and testing individual concerns, and a higher likelihood of introducing bugs during modifications. The component could become a bottleneck for future feature development.
- Fix approach: Refactor `ShipHistory.tsx` into smaller, more focused components or custom hooks. Extract map-related logic into a dedicated hook or utility, and consider separating data fetching concerns if they become more complex.

## Known Bugs

- Not detected

## Security Considerations

- Not detected

## Performance Bottlenecks

- Not detected

## Fragile Areas

- Not detected

## Scaling Limits

- Not detected

## Dependencies at Risk

- Not detected

## Missing Critical Features

- Not detected

## Test Coverage Gaps

- Not detected

---

*Concerns audit: 2026-04-14*