# Skill Self-Improvement Log — web-design-guidelines

## Summary
- **Start Score:** 22/25 (88%)
- **Final Score:** 25/25 (100%)
- **Total Iterations:** 3
- **Started:** 2026-03-16
- **Completed:** 2026-03-16

---

## Iterations

| # | Score | Failed Assertions | Change Made | Decision |
|---|-------|-------------------|-------------|----------|
| 1 | 22/25 | #4 (file:line format), #20 (WebFetch denied), #23 (preamble in T05) | Baseline — no changes | — |
| 2 | 23/25 | #15 (T03 over 200 words), #20 (WebFetch denied) | Added Output Format section: file:line example, no-preamble rule, word limits, ✓ pass format | KEEP (commit 067557e) |
| 3 | 25/25 | None | Added curl fallback when WebFetch unavailable | KEEP (commit 82201ab) |

---

## Change History

### Iteration 1 (Baseline)
- **Score:** 22/25 (88%)
- **Failed:**
  - #4: T01 used "line 5" instead of "Button.tsx:5" — skill lacked explicit format example
  - #20: T04 WebFetch denied — skill had no fallback mechanism
  - #23: T05 had long preamble before findings — skill didn't say "no preamble"
- **Change to SKILL.md:** None (baseline)
- **Decision:** N/A

### Iteration 2
- **Score:** 23/25 (92%)
- **Fixed:** #4 (file:line format), #23 (no preamble)
- **New failure:** #15 (T03 word count — agent over-reported non-typography issues)
- **Still failing:** #20 (WebFetch denied)
- **Change to SKILL.md:** Added `## Output Format` section with:
  - Explicit `filename.tsx:LINE` format with example
  - "Start directly with findings — no preamble" instruction
  - Word count limits (200 single-file, 400 multi-file)
  - `✓ filename — pass` format for clean files
- **Decision:** KEEP — net +1 (fixed 2, introduced 1 new failure)

### Iteration 3
- **Score:** 25/25 (100%)
- **Fixed:** #15 (T03 now terse/focused), #20 (curl fallback works)
- **Change to SKILL.md:** Added curl fallback in Guidelines Source:
  - "Try these methods in order: 1. WebFetch 2. Bash curl"
  - "Do not skip this step — always attempt the fetch"
- **Decision:** KEEP — all 25 assertions pass
