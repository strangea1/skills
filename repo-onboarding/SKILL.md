---
name: repo-onboarding
description: 'Generate or refresh a concise, agent-oriented repository overview using both Serena semantic/LSP analysis and repomap Tree-sitter/PageRank analysis. Use when onboarding an agent to an unfamiliar codebase, mapping architecture and module ownership, or replacing a verbose or stale codebase guide. Do not use for end-user setup guides or exhaustive API documentation.'
---

# Repository Onboarding

Create one compact Markdown map that lets an agent orient itself before making changes. The map is
a navigation layer over the repository, not a replacement for source code, `README`, `AGENTS.md`,
or task-specific investigation.

Use the language requested by the user. Otherwise follow the repository's primary documentation
language. Use a user-provided output path; otherwise update an existing concise codebase overview
referenced by repository instructions, or create `CODEBASE_OVERVIEW.md` at the repository root.

## Required analysis tools

Use both servers. They provide different evidence:

- **repomap** (`repo_map`, optionally `search_identifiers`): discover structural centers, related
  files, and likely subsystem boundaries from Tree-sitter definitions/references and PageRank.
- **Serena** (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`,
  `find_implementations`, `find_declaration`): verify exact symbols and semantic relationships with
  the active language server.

Read Serena's initial instructions before its first use and activate the repository project. Confirm
that the language server is ready. Existing Serena memories may be used as leads, but verify facts
against the current repository. Do not run Serena onboarding or modify memories merely to create
this document unless the user asks.

If either server is unavailable, do not silently claim a complete dual-source overview. Explain the
missing evidence and continue only if the user accepts a degraded result.

## Evidence policy

Use this order when facts disagree:

1. Current source code, manifests, task definitions, and scoped repository instructions.
2. Serena semantic results.
3. repomap output.
4. Existing overview documents or memories.

Treat repomap as discovery and prioritization, not proof of a runtime call chain. Verify every
claimed entry point, central abstraction, or cross-module execution path with Serena or a narrow
source read. Mark unresolved relationships as uncertain instead of guessing.

## Workflow

### 1. Establish scope and authority

1. Resolve the repository root and output path.
2. Read the root and nearest relevant instruction files.
3. Inspect only the minimum authoritative files needed to identify languages, workspace/package
   boundaries, task runners, and executable entry points.
4. Build a private coverage checklist from declared workspace/package members, binaries, services,
   SDKs, public protocol surfaces, and platform-specific roots. Group related support packages; the
   checklist is evidence for completeness, not content to paste into the output.
5. If the output already exists, preserve useful user-authored facts, but revalidate them and remove
   stale or duplicated material.

Do not edit `AGENTS.md`, `README`, Serena memories, or unrelated files unless explicitly requested.

### 2. Generate an unbiased repository map

Call `repo_map` without focus or priority inputs first. Use a token limit around 6,000-8,000 and
`excludeUnranked: true`. Keep the cache unless there is evidence that it is stale.

From the result, identify:

- major language/package roots;
- shared infrastructure with high cross-file centrality;
- likely entry points and public boundaries;
- clusters that represent distinct product or service domains.

Do not copy the raw map, ranks, scan counts, or long symbol lists into the document.

### 3. Generate one product-focused map

Use manifests, entry points, and the unbiased map to select a small set of likely product paths and
core identifiers. Call `repo_map` once more with roughly:

- 5-15 `priorityFiles`;
- 3-12 `priorityIdentifiers`;
- a token limit around 6,000-10,000;
- `excludeUnranked: true`.

Use `focusFiles` only for files already understood and intentionally excluded from output. Do not
keep adding map passes merely to increase confidence; add another only when a major subsystem or
primary execution path remains unresolved.

### 4. Verify with Serena

For each proposed major module and primary flow:

1. Use `get_symbols_overview` on candidate entry or ownership files.
2. Use `find_symbol` to confirm central functions, types, traits, or methods.
3. Use `find_referencing_symbols`, `find_implementations`, or `find_declaration` where the document
   claims a dependency, dispatch boundary, or implementation relationship.
4. Use a narrow source read only when generated code, macros, unsupported languages, or an LSP gap
   prevents semantic verification.

Before writing, reconcile the proposed module map with the coverage checklist. Every major product,
service, SDK, or public boundary must be represented or intentionally grouped under a named domain.
Low PageRank or exclusion from a token-budgeted map is not evidence that a declared module is
unimportant.

Distinguish these claims precisely:

- "owns or defines" does not imply "calls";
- a textual reference does not imply a runtime dependency;
- a public type does not imply it is an executable entry point;
- generated files do not define architectural ownership unless generation itself is central.

### 5. Write the compact map

Start from [the output template](./assets/onboarding-template.md), adapting sections to the actual
repository. Prefer links and routing guidance over copied details.

Default size budget:

- target: 1,500-2,500 estimated tokens;
- hard maximum: 3,000 estimated tokens or 250 lines;
- major module rows: usually 6-18, grouping small support packages by domain;
- architecture: at most 12 nodes;
- primary flows: 2-4;
- canonical commands: at most 10;
- recommended source entry points: at most 10.

For a large monorepo, cover every major domain by grouping related crates/packages. Do not enumerate
every directory, binary, RPC method, tool handler, test fixture, or generated type.

The document should contain:

1. project purpose and dominant technology/workspace shape;
2. a compact architecture diagram or equivalent text map;
3. all major module domains with ownership and key paths;
4. the primary execution/data flows an agent needs to navigate;
5. a change-routing table from task type to owning area and validation surface;
6. only the non-obvious invariants that affect where or how code is changed, linked to authority;
7. canonical build/test/format commands, linked to their task definition;
8. a short recommended reading path;
9. unresolved uncertainties only when they materially affect navigation.

Exclude:

- repo-map rank tables, scan statistics, cache details, and analysis dates;
- exhaustive file, crate, symbol, endpoint, or command catalogs;
- copied `AGENTS.md`, `README`, schema, or API prose;
- long installation tutorials and generic language guidance;
- volatile version numbers unless pinned and necessary to run the repository;
- line-number links, which become stale quickly;
- claims inferred only from names or directory layout.

Use relative Markdown links and verify every local target exists. Keep one fact in one place; link to
the authoritative source instead of repeating it in multiple sections.

### 6. Validate and report

Run the repository's formatter against only the output document when available. Then run:

```text
python <skill-directory>/scripts/validate_onboarding.py <output-document>
```

The validator checks the size budget, unfinished template markers, raw repomap leakage, and local
links. Fix all errors. Review the final diff for unsupported claims and accidental duplication.

Report the output path, whether both server passes completed, and any material uncertainty. Do not
paste the entire generated document into chat unless requested.