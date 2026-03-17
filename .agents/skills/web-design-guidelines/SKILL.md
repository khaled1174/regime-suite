---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

You MUST fetch the guidelines before reviewing any code. Try these methods in order:
1. Use WebFetch to retrieve the URL above
2. If WebFetch is unavailable, use Bash: `curl -sL "https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md"`

The fetched content contains all the rules and output format instructions. Do not skip this step — always attempt the fetch.

## Output Format

Start directly with findings — no preamble, no introduction, no summary of what you're about to do.

Use this exact format for every finding:

```
`filename.tsx:LINE` — Description of the issue. Suggested fix in active voice.
```

Example:
```
`Button.tsx:5` — Icon button missing `aria-label`. Add an `aria-label` describing the action.
```

Group findings under a `## filename` heading per file. If a file has zero issues, output `✓ filename — pass`.

Keep output terse: under 200 words for single-file reviews, under 400 for multi-file.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format above

If no files specified, ask the user which files to review.
