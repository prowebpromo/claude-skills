# Skill Description Trim — July 17, 2026

Follow-up to the [2026-07-16 skills audit](2026-07-16-skills-audit.md). That
audit fixed *routing* bugs (over-triggering, missing sibling exclusions);
this pass fixes *size*: the combined skill listing was blowing the context
budget Claude Code allots to it.

## Finding

Claude Code keeps every skill's name + description resident in context in
every session, budgeted at roughly **1% of the context window** (~2k tokens
on a 200k window ≈ 8k chars). The 18 custom skills' descriptions alone
totaled **16,783 chars (~4.2k est. tokens)** — with the built-in Anthropic
skills on top, the full listing sat at ~21.7k chars, about **2.5× over
budget**. When the listing exceeds budget, entries get truncated and skill
routing degrades — which defeats the purpose of the carefully written
trigger descriptions.

## What was done

Every custom description was rewritten to ~420–520 chars, keeping:

- the core purpose (one clause),
- the distinctive trigger phrases,
- **every sibling exclusion from the 2026-07-16 audit** — the
  fable-method ALONGSIDE framing (F1), the legal-only qualifier on
  legal-page-rewrite (F2), the gsc-sow-builder ↔ io-generator ↔
  diagnostic-builder ↔ csuite-report disambiguation web (F3), and the
  wp-classic-designer / legal-page-rewrite HTML-shell-vs-content boundary
  (F4),

and cutting synonym pile-ups, output-format detail, and redundant "also
trigger" examples.

Built-in Anthropic skills (docx, xlsx, pptx, pdf, skill-creator) and the
small bundled ones (morning, session-start-hook) were left untouched.

## Scorecard (description chars, before → after)

| Skill | Before | After |
|---|---|---|
| ai-visibility-trends | 873 | 454 |
| csuite-report | 867 | 487 |
| diagnostic-builder | 873 | 521 |
| entitymap-generator | 883 | 423 |
| fable-method | 845 | 496 |
| gbp-optimization | 1022 | 515 |
| geo-master-blueprint | 1016 | 517 |
| gsc-sow-builder | 926 | 460 |
| internal-linking | 1012 | 504 |
| io-generator | 852 | 517 |
| legal-page-rewrite | 1029 | 503 |
| ppc-sow-builder | 909 | 503 |
| proposal-builder | 1006 | 461 |
| scored-eval | 999 | 500 |
| sitebulb-sow-builder | 909 | 453 |
| social-ai-team | 883 | 427 |
| social-performance-review | 931 | 441 |
| wp-classic-designer | 948 | 438 |
| **Total** | **16,783** | **8,620** |

**Saved: 8,163 chars ≈ 2,040 est. resident tokens per session.** The full
listing (custom + built-ins) lands at ~13.5k chars (~3.4k est. tokens) —
near budget; the remainder is Anthropic-maintained descriptions we can't
edit.

## How to apply

The trimmed texts ship in
[`tools/skills-manager/trim_fixes.json`](../tools/skills-manager/trim_fixes.json).
From a machine with your `ANTHROPIC_API_KEY` set (same account as your
claude.ai login):

```bash
cd tools/skills-manager
python skills_manager.py apply-audit --fixes trim_fixes.json --dry-run   # preview
python skills_manager.py apply-audit --fixes trim_fixes.json             # apply
```

The 9 skills from the July 16 audit are pinned to their skill IDs; the
other 9 resolve by name from the live listing. Each update creates a new
skill version — old versions stay available for rollback via the Skills
API. The [`fixes/`](../fixes/) directory holds the same texts as
copy-paste fallback (claude.ai → Settings → Capabilities → Skills).

## Risk note

Shorter descriptions trade recall for budget: a niche phrasing that only
matched a cut synonym may no longer trigger the skill. If a skill stops
firing on a phrasing you actually use, add that one phrase back to its
description rather than reverting the whole trim.
