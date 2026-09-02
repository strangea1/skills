# {{PROJECT_NAME}} codebase map

> {{ONE_SENTENCE_PURPOSE_AND_SCOPE}}

## At a glance

- **Primary stack:** {{LANGUAGES_AND_RUNTIME}}
- **Workspace shape:** {{WORKSPACE_OR_PACKAGE_BOUNDARIES}}
- **Main entry points:** {{EXECUTABLE_OR_SERVICE_ENTRY_POINTS}}
- **Authority:** {{LINKS_TO_INSTRUCTIONS_MANIFESTS_AND_TASK_RUNNER}}

## Architecture

{{COMPACT_MERMAID_DIAGRAM_OR_TEXT_MAP_MAX_12_NODES}}

## Module map

| Domain | Owns | Key paths |
| --- | --- | --- |
| {{MAJOR_DOMAIN}} | {{RESPONSIBILITY_NOT_IMPLEMENTATION_DETAIL}} | {{RELATIVE_LINKS}} |

Group related support packages. Include every major product or service domain, not every directory.

## Primary flows

1. **{{FLOW_NAME}}:** {{ENTRY_TO_CORE_TO_OUTPUT_WITH_VERIFIED_LINKS}}
2. **{{FLOW_NAME}}:** {{ENTRY_TO_CORE_TO_OUTPUT_WITH_VERIFIED_LINKS}}

## Change routing

| Change type | Owning area | Focused validation |
| --- | --- | --- |
| {{TASK_CATEGORY}} | {{RELATIVE_LINKS}} | {{CANONICAL_NARROW_CHECK}} |

## Non-obvious invariants

- {{INVARIANT_THAT_CHANGES_AGENT_DECISIONS_WITH_AUTHORITY_LINK}}

## Canonical commands

```text
{{ONLY_THE_ESSENTIAL_RUN_BUILD_TEST_FORMAT_COMMANDS}}
```

## Read next

1. {{ENTRY_OR_ARCHITECTURE_FILE_LINK_AND_WHY}}
2. {{CORE_FLOW_FILE_LINK_AND_WHY}}
3. {{BOUNDARY_OR_PROTOCOL_FILE_LINK_AND_WHY}}

## Material uncertainties

- {{ONLY_UNRESOLVED_FACTS_THAT_AFFECT_NAVIGATION_OR_REMOVE_THIS_SECTION}}