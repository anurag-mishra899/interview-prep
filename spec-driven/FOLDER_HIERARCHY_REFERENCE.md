# Spec-Driven Development: Folder Hierarchy Reference

**Quick Reference Guide for Enterprise Implementation**

---

## Overview

This document provides side-by-side folder hierarchy comparisons for different SDD adoption contexts and maturity levels.

---

## 1. Greenfield vs Brownfield vs Legacy

### Visual Comparison

```
GREENFIELD                      BROWNFIELD                       LEGACY MODERNIZATION
(Start from scratch)            (Add to existing)                (Replace old system)

project-root/                   existing-project/                legacy-migration/
├── .specify/                   ├── src/ (UNCHANGED)             ├── legacy/ (READ-ONLY)
│   ├── memory/                 │   ├── controllers/             │   └── src/
│   │   ├── constitution.md     │   ├── models/                  │
│   │   ├── architecture.md     │   └── services/                ├── .specify/
│   │   └── tech-stack.md       │                                │   ├── memory/
│   │                           ├── .specify/ (NEW)              │   │   ├── constitution.md
│   ├── specs/                  │   ├── memory/                  │   │   ├── legacy-context.md
│   │   ├── 001-auth/           │   │   ├── constitution.md      │   │   └── parity-requirements.md
│   │   │   ├── spec.md         │   │   ├── existing-arch.md     │   │
│   │   │   ├── plan.md         │   │   └── migration.md         │   ├── specs/
│   │   │   └── tasks.md        │   │                            │   │   ├── 001-user-mgmt/
│   │   └── 002-payments/       │   ├── specs/ (NEW FEATURES)    │   │   │   ├── spec.md
│   │                           │   │   ├── 001-new-x/           │   │   │   ├── legacy-analysis.md
│   └── templates/              │   │   └── 002-new-y/           │   │   │   ├── parity-checklist.md
│                               │   │                            │   │   │   └── plan.md
├── src/                        │   └── specs-retro/ (OPTIONAL)  │   │   └── 002-orders/
│   ├── libs/                   │       └── existing-auth/       │   │
│   │   ├── auth/               │                                │   └── specs-experiments/
│   │   └── payments/           ├── tests/ (EXISTING)            │       └── 901-graphql/
│   │                           └── docs/                        │
│   └── apps/                                                    ├── modern/ (NEW)
│       └── web/                Status: HYBRID                   │   ├── services/
│                               - Old code: Traditional          │   │   ├── user-service/
├── tests/                      - New code: Spec-Driven          │   │   └── order-service/
└── docs/                                                        │   └── frontend/
                                                                 │
Status: FULL SDD                                                 └── migration/
- All code via specs                                                 └── cutover-scripts/

                                                                 Status: PARALLEL SYSTEMS
                                                                 - Legacy: Deprecated
                                                                 - Modern: Active development
```

---

## 2. Maturity Level Evolution

### Spec-First → Spec-Anchored → Spec-as-Source

```
SPEC-FIRST                      SPEC-ANCHORED                    SPEC-AS-SOURCE
(Learning & Prototypes)         (Production Features)            (Strategic Components)

project-root/                   project-root/                    project-root/
├── .specify/                   ├── .specify/                    ├── .specify/
│   ├── specs/                  │   ├── specs/                   │   ├── specs/
│   │   └── 001-spike/          │   │   ├── 001-auth/            │   │   ├── 001-api-gateway/
│   │       ├── spec.md         │   │   │   ├── spec.md          │   │   │   ├── spec.md ⭐
│   │       ├── plan.md         │   │   │   ├── plan.md          │   │   │   ├── plan.md
│   │       └── tasks.md        │   │   │   └── tasks.md         │   │   │   └── tasks.md
│   │                           │   │   │                        │   │   │
│   └── templates/              │   │   └── 002-payments/        │   │   └── 002-data-layer/
│                               │   │       └── ... (kept)        │   │       └── ... (maintained)
├── src/                        │   │                            │   │
│   └── spike/ ⚡               │   ├── extensions/               │   ├── extensions/
│       (Disposable)            │   │   └── spec-kit-sync/       │   │   ├── spec-kit-sync/
│                               │   │                            │   │   └── code-gen-validator/
└── tests/                      │   └── templates/               │   │
    └── spike-tests/            │                                │   └── scripts/
                                ├── src/                         │       └── regenerate-all.sh
Lifecycle:                      │   ├── libs/                    │
1. Create spec                  │   │   ├── auth/                ├── src/
2. Implement                    │   │   │   └── index.ts         │   ├── generated/ ⚠️
3. Ship                         │   │   │       (human-edited)   │   │   ├── api-gateway/
4. DELETE SPEC ✂️               │   │   │                        │   │   │   ├── index.ts
                                │   │   └── payments/            │   │   │   │   // GENERATED - DO NOT EDIT
Git:                            │   │       └── index.ts         │   │   │   │   // Source: specs/001/spec.md
- Specs not committed           │   │           (human-edited)   │   │   │   └── routes.ts
- Code committed                │   │                            │   │   │
                                │   └── apps/                    │   │   └── data-layer/
Flexibility: HIGHEST            │                                │   │       └── ... (generated)
Maintenance: NONE               ├── tests/                       │   │
Review: Code only               │                                │   └── custom/ (human-written)
                                └── .github/workflows/           │       └── middleware/
                                    └── drift-detection.yml      │
                                                                 ├── tests/
Lifecycle:                      Lifecycle:                       │   ├── generated/
1. Create spec                  1. Create spec                   │   │   └── ... (from spec)
2. Implement                    2. Implement                     │   └── integration/
3. Ship                         3. Ship                          │
4. KEEP SPEC 📌                 4. KEEP SPEC 📌                  └── .github/workflows/
5. Update spec on changes       5. Update spec + code            │   ├── regenerate-on-spec-change.yml
6. Manually sync                6. Detect drift                  │   └── validate-no-manual-edits.yml

Git:                            Git:                             Lifecycle:
- Specs committed               - Specs committed                1. Create spec
- Code committed                - Code committed                 2. GENERATE CODE 🤖
- Both reviewed in PRs          - Both reviewed in PRs           3. Ship
                                - Drift alerts                   4. ONLY EDIT SPEC ⭐
Flexibility: HIGH                                                5. REGENERATE CODE 🔄
Maintenance: MODERATE           Flexibility: MEDIUM              6. Never manually edit generated/
Review: Spec + Code             Maintenance: HIGH
                                Review: Spec + Code + Drift      Git:
                                                                 - Specs committed (primary)
                                                                 - Generated code committed (secondary)
                                                                 - Only specs reviewed in PRs

                                                                 Flexibility: LOWEST
                                                                 Maintenance: SPEC ONLY
                                                                 Review: Spec only (code is artifact)
```

---

## 3. Extension & Preset Priority

### Template Resolution Order

```
PROJECT STRUCTURE               PRIORITY ORDER                   EXAMPLE OVERRIDE

project-root/                   ┌─────────────────────┐
├── .specify/                   │ 1. OVERRIDES        │ (Highest Priority)
│   │                           │    Project-local    │
│   ├── templates/              │    customizations   │
│   │   └── overrides/ ⭐ ←───── └─────────────────────┘
│   │       ├── spec.md
│   │       └── plan.md         ┌─────────────────────┐
│   │                           │ 2. PRESETS          │
│   ├── presets/ ⭐ ←───────────── │    Methodology-    │
│   │   ├── agile-scrum/       │    specific         │
│   │   │   └── templates/     └─────────────────────┘
│   │   │       └── spec.md
│   │   │                      ┌─────────────────────┐
│   │   └── compliance-soc2/   │ 3. EXTENSIONS       │
│   │       └── templates/     │    Feature add-ons  │
│   │           └── plan.md    └─────────────────────┘
│   │
│   ├── extensions/ ⭐ ←───────── Lookup order:
│   │   ├── spec-kit-jira/     1. Check overrides/spec.md
│   │   │   └── templates/     2. If not found, check presets/*/templates/spec.md
│   │   │       └── spec.md    3. If not found, check extensions/*/templates/spec.md
│   │   │                      4. If not found, use core templates/spec.md
│   │   └── spec-kit-security/
│   │       └── templates/     ┌─────────────────────┐
│   │           └── plan.md    │ 4. CORE (spec-kit)  │
│   │                          │    Baseline         │
│   └── templates/ ⭐ ←───────── └─────────────────────┘ (Lowest Priority)
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md

CUSTOMIZATION STRATEGY:

1️⃣  OVERRIDE for one project only
   Use: .specify/templates/overrides/

2️⃣  PRESET for organizational standards
   Use: .specify/presets/ (install via preset add)
   Examples: agile-scrum, compliance-soc2, security-first

3️⃣  EXTENSION for new capabilities
   Use: .specify/extensions/ (install via extension add)
   Examples: jira integration, CI guards, drift detection

4️⃣  CORE never modify directly
   Managed by spec-kit version
```

---

## 4. Team Size Adaptations

### Small vs Medium vs Large Enterprise

```
SMALL TEAM (3-5)                MEDIUM TEAM (6-15)               LARGE ENTERPRISE (16+)
Single-track model              Dual-track model                 Specialized roles

project-root/                   project-root/                    organization/
├── .specify/                   ├── .specify/                    ├── corporate/
│   ├── memory/                 │   ├── memory/                  │   ├── constitution.md ⭐
│   │   └── constitution.md     │   │   ├── constitution.md      │   │   (Corporate-wide)
│   │                           │   │   ├── product-vision.md    │   │
│   ├── specs/                  │   │   └── architecture.md      │   ├── presets/
│   │   ├── 001-feature-a/      │   │                            │   │   ├── compliance-soc2/
│   │   │   └── ... (Alice)     │   ├── specs/                   │   │   ├── security-baseline/
│   │   ├── 002-feature-b/      │   │   ├── 001-auth/            │   │   └── agile-scrum/
│   │   │   └── ... (Bob)       │   │   │   └── ... (Spec Team)  │   │
│   │   └── 003-feature-c/      │   │   ├── 002-payments/        │   └── extensions/
│   │       └── ... (Carol)     │   │   │   └── ... (Spec Team)  │       └── corp-jira/
│   │                           │   │   └── 003-reporting/       │
│   └── extensions/             │   │       └── ... (Spec Team)  ├── platform-team/
│       └── team-basics/        │   │                            │   └── custom-extensions/
│                               │   ├── plans/                   │       └── spec-kit-corp/
│                               │   │   ├── 001-auth/            │
Roles:                          │   │   │   └── ... (Arch Team)  ├── product-1/
- Everyone: All roles           │   │   ├── 002-payments/        │   ├── .specify/
- Rotating: Reviewer            │   │   │   └── ... (Arch Team)  │   │   ├── memory/
- Rotating: Constitutional      │   │   └── 003-reporting/       │   │   │   └── constitution.md
│           Steward             │   │       └── ... (Arch Team)  │   │   │       (inherits corporate)
│                               │   │                            │   │   │
Process:                        │   └── implementations/         │   │   ├── specs/ (Product Eng)
1. Anyone writes spec           │       ├── 001-auth/            │   │   ├── plans/ (Solution Arch)
2. Peer review                  │       │   └── ... (Dev Team)   │   │   └── tasks/ (Feature Teams)
3. Same person plans            │       ├── 002-payments/        │   │
4. Same person implements       │       │   └── ... (Dev Team)   │   └── src/
5. Peer review code             │       └── 003-reporting/       │
                                │           └── ... (Dev Team)   ├── product-2/
Tools:                          │                                │   └── ... (same structure)
- Core spec-kit only            Roles:                           │
- Minimal extensions            - Spec Team: Write specs         └── platform/
                                - Arch Team: Design plans            └── shared-libs/
Coordination:                   - Dev Team: Implement
- Daily standup                 - QA Team: Review drift          Roles:
- Shared Slack channel          - Platform: Extensions           - Product Engineers: Specs
                                                                 - Solution Architects: Plans
                                Process:                         - Feature Teams: Implement
                                1. Spec Team writes spec         - Platform Team: Tooling
                                2. Arch Team reviews + plans     - Quality Eng: Validation
                                3. Dev Team implements
                                4. QA validates + drift check    Process:
                                5. Platform maintains tools      1. Product Eng → Spec
                                                                 2. Solution Arch → Plan
                                Tools:                           3. Feature Team → Implement
                                - Full extension suite           4. Quality Eng → Validate
                                - CI/CD integration              5. Platform → Support
                                - Custom presets
                                                                 Tools:
                                Coordination:                    - Corporate preset mandatory
                                - Weekly spec review             - Custom corp extensions
                                - Architecture guild             - Full CI/CD pipeline
                                - Bi-weekly drift review         - Centralized monitoring

                                                                 Coordination:
                                                                 - Cross-product guild
                                                                 - Quarterly spec summit
                                                                 - Platform office hours
```

---

## 5. CI/CD Integration Patterns

### File Structure with Validation Hooks

```
project-root/
├── .specify/
│   ├── specs/
│   │   └── 001-feature/
│   │       ├── spec.md
│   │       ├── plan.md
│   │       └── tasks.md
│   │
│   └── extensions/
│       ├── spec-kit-ci-guard/           # Gate 1: Spec exists
│       ├── spec-kit-sync/               # Gate 2: Drift detection
│       ├── spec-kit-security/           # Gate 3: Security review
│       └── spec-kit-constitution/       # Gate 4: Constitutional compliance
│
├── .github/
│   ├── workflows/
│   │   ├── 01-spec-validation.yml ──────┐
│   │   │   # Runs on PR to .specify/     │
│   │   │   # - Spec completeness check   │
│   │   │   # - Constitutional compliance │
│   │   │                                 │
│   │   ├── 02-plan-review-gate.yml ──────┤
│   │   │   # Requires human approval     ├─── PR GATES
│   │   │   # - Architect sign-off        │
│   │   │   # - Security review           │
│   │   │                                 │
│   │   ├── 03-implementation-check.yml ──┤
│   │   │   # Runs on PR to src/          │
│   │   │   # - Drift detection           │
│   │   │   # - Test coverage             │
│   │   │                                 │
│   │   └── 04-post-merge.yml ────────────┘
│   │       # Update Jira tickets
│   │       # Generate changelog
│   │       # Notify stakeholders
│   │
│   └── CODEOWNERS
│       # .specify/memory/constitution.md @architects
│       # .specify/specs/**/spec.md @product-team
│       # .specify/specs/**/plan.md @architects
│
├── src/                                 # Implementation
│   └── ... (generated or hand-written)
│
└── tests/
    ├── unit/                            # Article III compliance
    ├── integration/                     # Article IX compliance
    └── contract/                        # API contract validation

CI/CD FLOW:

┌─────────────────────────────────────────────────────────────────┐
│ Developer Workflow                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. /speckit.specify → spec.md created                          │
│     └─ PR #1: spec.md only                                      │
│        ├─ Gate: Spec completeness check ✓                       │
│        ├─ Gate: Constitutional compliance ✓                     │
│        └─ Review: Product Team ✓                                │
│           └─ MERGE                                              │
│                                                                 │
│  2. /speckit.plan → plan.md created                             │
│     └─ PR #2: plan.md only                                      │
│        ├─ Gate: Technical feasibility ✓                         │
│        ├─ Gate: Security review ✓                               │
│        └─ Review: Architects ✓                                  │
│           └─ MERGE                                              │
│                                                                 │
│  3. /speckit.implement → src/ code created                      │
│     └─ PR #3: src/ + tests/                                     │
│        ├─ Gate: Spec-code drift check ✓                         │
│        ├─ Gate: Test coverage ≥80% ✓                            │
│        ├─ Gate: TDD compliance ✓                                │
│        └─ Review: Dev Team ✓                                    │
│           └─ MERGE                                              │
│                                                                 │
│  4. Post-Merge Automation                                       │
│     ├─ Update Jira ticket → DONE                                │
│     ├─ Generate changelog entry                                 │
│     ├─ Notify stakeholders                                      │
│     └─ Deploy to staging                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Constitutional Article Enforcement

### File Structure for Compliance Tracking

```
project-root/
├── .specify/
│   ├── memory/
│   │   ├── constitution.md ─────────────┐
│   │   │   # Article I: Library-First   │
│   │   │   # Article II: CLI Interface  │  ENFORCED VIA:
│   │   │   # Article III: Test-First    │
│   │   │   # Article VII: Simplicity    │
│   │   │   # Article VIII: Anti-Abstr   │
│   │   │   # Article IX: Integration    │
│   │   │                                │
│   │   └── complexity-budget.md ────────┤
│   │       # Track Article VII          │
│   │       # compliance                 │
│   │                                    │
│   ├── specs/001-feature/               │
│   │   ├── spec.md                      │
│   │   ├── plan.md ──────────────────┐  │
│   │   │   ## Constitutional Gates   │  │
│   │   │   ### Article I: ✓          │  │
│   │   │   - Implemented as lib/auth │  │
│   │   │   ### Article III: ✓        │  │
│   │   │   - Tests in tasks.md       │  │
│   │   │   ### Article VII: ✓        │◄─┤
│   │   │   - 2 projects (≤3)         │  │
│   │   │                             │  │
│   │   └── tasks.md ──────────────┐  │  │
│   │       ## Task 1: Write Tests  │  │  │
│   │       ## Task 2: Implement    │◄─┤  │
│   │       ## Task 3: Refactor     │  │  │
│   │                               │  │  │
│   └── extensions/                 │  │  │
│       └── spec-kit-constitution/  │  │  │
│           └── validate.sh ─────────┼──┼──┘
│                                   │  │
├── src/                            │  │
│   ├── libs/ ◄──────────────────────┘  │ (Article I)
│   │   └── auth/                      │
│   │       ├── cli.ts ◄─────────────────┘ (Article II)
│   │       └── index.ts
│   │
│   └── apps/
│       └── web/
│           └── uses libs/ only ◄────── (Article I)
│
└── tests/ ◄──────────────────────────── (Article III)
    ├── unit/
    │   └── auth.test.ts (written first)
    │
    └── integration/
        └── auth.integration.test.ts ◄── (Article IX)

ENFORCEMENT MECHANISMS:

1️⃣  Template-Driven (Preventative)
   - spec.md template includes constitutional checklist
   - plan.md template enforces gates
   - tasks.md template mandates test-first order

2️⃣  CI/CD Validation (Detective)
   - spec-kit-constitution extension runs in CI
   - Validates file structure (libs/ exists)
   - Checks test coverage (Article III)
   - Counts projects (Article VII ≤3)

3️⃣  Human Review (Corrective)
   - CODEOWNERS requires architect approval
   - Plan review checklist
   - Constitutional violation escalation

4️⃣  Metrics Dashboard (Monitoring)
   - Article I compliance: % features as libs
   - Article III compliance: Test coverage
   - Article VII compliance: Project count trend
```

---

## 7. Quick Reference: Choose Your Structure

### Decision Matrix

| Your Situation | Recommended Folder Structure | See Section |
|---------------|------------------------------|-------------|
| **New project, team learning SDD** | Greenfield (Spec-First) | Section 1, Column 1 |
| **New product, production-ready** | Greenfield (Spec-Anchored) | Section 1, Column 1 + Section 2, Column 2 |
| **Existing codebase, add SDD** | Brownfield (Hybrid) | Section 1, Column 2 |
| **Migrating legacy system** | Legacy Modernization (Parallel) | Section 1, Column 3 |
| **Small team (3-5 developers)** | Small Team (Single-track) | Section 4, Column 1 |
| **Medium team (6-15 developers)** | Medium Team (Dual-track) | Section 4, Column 2 |
| **Large enterprise (16+)** | Large Enterprise (Specialized) | Section 4, Column 3 |
| **Exploration phase** | Spec-First (Disposable) | Section 2, Column 1 |
| **Production features** | Spec-Anchored (Maintained) | Section 2, Column 2 |
| **Strategic components** | Spec-as-Source (Generated) | Section 2, Column 3 |

---

## 8. Common Mistakes to Avoid

### Anti-Patterns in Folder Organization

❌ **WRONG: Mixing spec maturity levels in one directory**
```
.specify/specs/
├── 001-auth/           # Spec-anchored
├── 002-payments/       # Spec-first (will be deleted)
└── 003-api-gateway/    # Spec-as-source
```

✅ **RIGHT: Separate by lifecycle**
```
.specify/
├── specs/              # Spec-anchored (production)
│   ├── 001-auth/
│   └── 003-api-gateway/
└── experiments/        # Spec-first (disposable)
    └── spike-payments/
```

---

❌ **WRONG: Brownfield trying to retrofit everything**
```
.specify/specs/
├── 001-existing-auth/      # Reverse-engineered
├── 002-existing-orders/    # Reverse-engineered
├── 003-existing-payments/  # Reverse-engineered
└── 004-new-feature/        # Actually new
```

✅ **RIGHT: Focus on forward-looking work**
```
.specify/
├── specs/                  # NEW features only
│   └── 001-notifications/
└── docs/
    └── existing-arch.md    # Document, don't spec
```

---

❌ **WRONG: No separation of concerns**
```
project-root/
├── specs/          # Mixed memory bank + feature specs
│   ├── constitution.md
│   ├── architecture.md
│   ├── feature-auth.md
│   └── feature-payments.md
```

✅ **RIGHT: Clear separation**
```
.specify/
├── memory/                 # Long-lived context
│   ├── constitution.md
│   └── architecture.md
└── specs/                  # Feature-specific
    ├── 001-auth/
    └── 002-payments/
```

---

❌ **WRONG: Committing generated code without markers**
```
src/
└── api-gateway/
    └── routes.ts           # Is this generated or hand-written?
```

✅ **RIGHT: Clear generated vs custom separation**
```
src/
├── generated/              # ⚠️ DO NOT EDIT
│   └── api-gateway/
│       └── routes.ts       # // GENERATED FROM SPEC
└── custom/                 # ✅ Human-written
    └── middleware/
        └── auth.ts
```

---

## 9. Template Customization Examples

### Override Hierarchy in Practice

**Scenario:** Enterprise requires SOC2 compliance gates in all plans

```
.specify/
├── templates/                      # Core (spec-kit baseline)
│   ├── spec.md                     # Generic spec template
│   └── plan.md                     # Generic plan template
│
├── presets/                        # Organizational standards
│   └── compliance-soc2/
│       └── templates/
│           └── plan.md ⭐          # ADDS: SOC2 checklist
│               ## SOC2 Compliance
│               - [ ] Data encryption at rest
│               - [ ] Access control implemented
│               - [ ] Audit logging enabled
│
├── extensions/                     # Feature add-ons
│   └── spec-kit-jira/
│       └── templates/
│           └── spec.md ⭐          # ADDS: Jira ticket fields
│               ## Jira Integration
│               - Epic: [KEY-123]
│               - Story Points: 5
│
└── templates/overrides/            # Project-specific
    └── plan.md ⭐                  # ADDS: Project tech constraints
        ## Project Constraints
        - MUST use internal auth library v2.x
        - CANNOT use external APIs without security review

RESULTING plan.md WHEN RUNNING /speckit.plan:

Includes (in order):
1. Project constraints (overrides)
2. SOC2 checklist (preset)
3. Generic sections (core)

Excludes:
- Jira fields (only in spec.md)
```

---

## Conclusion

This reference guide provides the essential folder structures for all SDD adoption scenarios. Key principles:

1. **Greenfield**: Full `.specify/` structure from day 1
2. **Brownfield**: Add `.specify/` alongside existing code, hybrid workflow
3. **Legacy**: Parallel `legacy/` (read-only) and `modern/` (active)
4. **Maturity**: Separate disposable (spec-first) from living (spec-anchored/spec-as-source)
5. **Team Size**: Adapt hierarchy to team structure (single-track → dual-track → specialized)
6. **Compliance**: Use presets for organizational standards, overrides for project-specific

**Next Steps:**
1. Identify your context (greenfield/brownfield/legacy)
2. Choose maturity level (spec-first/anchored/as-source)
3. Copy relevant structure from this guide
4. Customize with presets/overrides for your organization
5. Iterate based on team feedback

---

**Document Version:** 1.0
**Companion To:** ENTERPRISE_ADOPTION_GUIDE.md
**Last Updated:** April 24, 2026
