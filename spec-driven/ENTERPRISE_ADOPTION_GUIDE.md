# Spec-Driven Development: Enterprise Adoption Guide

**Consultant Report: Strategic Implementation Across Enterprise Contexts**

---

## Executive Summary

Spec-Driven Development (SDD) represents a **paradigm inversion** where specifications become executable artifacts that generate code, rather than documentation that guides it. This report provides enterprise-grade guidance for adopting SDD across three critical contexts:

- **Greenfield Projects**: Starting new initiatives with SDD-first architecture
- **Brownfield Projects**: Introducing SDD into existing, active codebases
- **Modern Legacy**: Applying SDD to legacy modernization and technology pivots

### Key Finding

Enterprise adoption requires **progressive maturity** across three implementation levels:
1. **Spec-First** → Exploration & Learning (low commitment)
2. **Spec-Anchored** → Production Features (medium commitment)
3. **Spec-as-Source** → Strategic Components (high commitment)

---

## 1. Enterprise Adoption Strategy Matrix

### 1.1 Decision Framework

| Context | Recommended Approach | Maturity Level | Risk Profile |
|---------|---------------------|----------------|--------------|
| **Greenfield - New Product** | Spec-Anchored from Day 1 | Medium-High | Low |
| **Greenfield - Prototype/POC** | Spec-First (disposable) | Low | Very Low |
| **Brownfield - New Features** | Spec-First → Spec-Anchored | Medium | Medium |
| **Brownfield - Major Refactor** | Reverse Engineer → Spec-Anchored | Medium | High |
| **Legacy - Feature Parity** | Spec-First Documentation | Low-Medium | Medium |
| **Legacy - Tech Stack Pivot** | Spec-Anchored Rewrite | High | High |
| **Legacy - Incremental Modernization** | Hybrid (Traditional + Spec-First) | Low | Low |

### 1.2 Adoption Velocity Recommendations

**Phase 1 (Months 1-3): Exploration**
- 1-2 greenfield spikes using Spec-First
- Team training on constitutional principles
- Tool evaluation (spec-kit, Kiro, Tessl)
- Internal case studies

**Phase 2 (Months 4-6): Selective Production**
- New features only (no brownfield)
- Spec-Anchored for critical paths
- Establish spec review practices
- Measure: time to delivery, quality metrics, team satisfaction

**Phase 3 (Months 7-12): Scaled Adoption**
- Brownfield feature development
- Extension ecosystem integration
- CI/CD gates and validation
- Optional: Spec-as-Source for select components

**Phase 4 (Year 2+): Strategic Optimization**
- Legacy modernization initiatives
- Custom extensions and presets
- Cross-team constitutional alignment
- Advanced workflows (MAQA, Fleet)

---

## 2. Greenfield Projects: SDD-First Architecture

### 2.1 Ideal Folder Hierarchy - Greenfield

```
project-root/
├── .specify/                          # Spec Kit workspace
│   ├── memory/                        # Long-lived project context
│   │   ├── constitution.md            # Project principles (IMMUTABLE)
│   │   ├── AGENTS.md                  # AI agent guidance
│   │   ├── architecture.md            # High-level architecture decisions
│   │   ├── tech-stack.md              # Technology choices & rationale
│   │   └── glossary.md                # Domain terminology
│   │
│   ├── specs/                         # Feature specifications
│   │   ├── 001-user-authentication/   # Spec #001
│   │   │   ├── spec.md                # Requirements (WHAT & WHY)
│   │   │   ├── plan.md                # Implementation plan (HOW)
│   │   │   ├── tasks.md               # Executable task list
│   │   │   ├── research.md            # Technology research notes
│   │   │   ├── data-model.md          # Database schema, entities
│   │   │   ├── quickstart.md          # Developer onboarding for this feature
│   │   │   └── contracts/             # API contracts & schemas
│   │   │       ├── api-spec.json      # OpenAPI/GraphQL schema
│   │   │       ├── events.md          # Event definitions
│   │   │       └── integrations.md    # External service contracts
│   │   │
│   │   ├── 002-payment-processing/    # Spec #002
│   │   │   └── ... (same structure)
│   │   │
│   │   └── 003-notification-system/   # Spec #003
│   │       └── ... (same structure)
│   │
│   ├── templates/                     # Core templates (DO NOT EDIT)
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── tasks-template.md
│   │
│   ├── templates/overrides/           # Project-specific customizations
│   │   ├── spec-template.md           # Custom spec format
│   │   └── tasks-template.md          # Custom task structure
│   │
│   ├── presets/                       # Installed methodology presets
│   │   ├── agile-scrum/               # Scrum-based workflow
│   │   ├── compliance-soc2/           # SOC2 compliance gates
│   │   └── security-review/           # Security checklist integration
│   │
│   ├── extensions/                    # Installed community extensions
│   │   ├── spec-kit-jira/             # Jira integration
│   │   ├── spec-kit-ci-guard/         # CI validation
│   │   └── spec-kit-security/         # Security scanning
│   │
│   └── scripts/                       # Automation scripts
│       ├── create-new-feature.sh      # Feature scaffolding
│       ├── setup-plan.sh              # Plan initialization
│       └── common.sh                  # Shared utilities
│
├── .github/                           # GitHub-specific
│   ├── prompts/                       # AI agent commands (GitHub Copilot)
│   │   ├── speckit.constitution.md
│   │   ├── speckit.specify.md
│   │   ├── speckit.clarify.md
│   │   ├── speckit.plan.md
│   │   ├── speckit.tasks.md
│   │   └── speckit.implement.md
│   │
│   └── workflows/                     # CI/CD pipelines
│       ├── spec-validation.yml        # Validate specs before merge
│       ├── spec-drift-detection.yml   # Detect spec-code drift
│       └── plan-review-gate.yml       # Require plan approval
│
├── .claude/                           # Claude Code specific
│   └── commands/                      # Slash commands for Claude
│       ├── speckit.constitution.md
│       ├── speckit.specify.md
│       └── ... (mirrors .github/prompts)
│
├── src/                               # Source code (generated/maintained)
│   ├── libs/                          # Feature libraries (Article I)
│   │   ├── auth/                      # From spec 001
│   │   ├── payments/                  # From spec 002
│   │   └── notifications/             # From spec 003
│   │
│   ├── apps/                          # Applications
│   │   ├── web/                       # Web application
│   │   ├── mobile/                    # Mobile app
│   │   └── admin/                     # Admin portal
│   │
│   └── shared/                        # Shared utilities
│       ├── types/
│       ├── utils/
│       └── config/
│
├── tests/                             # Test suites
│   ├── unit/                          # Unit tests (TDD - Article III)
│   ├── integration/                   # Integration tests (Article IX)
│   ├── e2e/                           # End-to-end tests
│   └── contract/                      # Contract tests
│
├── docs/                              # Human-readable documentation
│   ├── architecture/                  # Architecture decision records (ADRs)
│   ├── runbooks/                      # Operational guides
│   └── api/                           # API documentation (generated)
│
├── .gitignore
├── README.md                          # Project overview
└── package.json / requirements.txt / etc.
```

### 2.2 Greenfield Workflow

**Constitutional Setup (One-time)**
```bash
# 1. Initialize project
specify init my-product --ai copilot

# 2. Establish constitutional foundation
/speckit.constitution Create principles for:
- Library-first architecture (Article I)
- CLI interface mandate (Article II)
- Test-first development (Article III)
- Simplicity (max 3 projects initially - Article VII)
- Anti-abstraction (trust frameworks - Article VIII)
- Integration-first testing (Article IX)
```

**Per-Feature Development Cycle**
```bash
# 3. Specify feature requirements (WHAT & WHY only)
/speckit.specify Build user authentication system with email/password and OAuth2 support

# 4. Clarify underspecified areas
/speckit.clarify

# 5. Create technical implementation plan (NOW specify HOW)
/speckit.plan Use Passport.js for auth, PostgreSQL for user storage, Redis for sessions

# 6. Generate task breakdown
/speckit.tasks

# 7. Execute implementation
/speckit.implement
```

**Time Comparison**
- Traditional: ~12 hours (PRD → Design → Specs → Tests → Implementation)
- SDD with spec-kit: ~15-30 minutes for spec artifacts, then implementation

### 2.3 Greenfield Best Practices

✅ **Do:**
- Establish constitution BEFORE first feature
- Use semantic spec numbering (001, 002, 003...)
- Create dedicated branches per spec (`001-feature-name`)
- Review specs BEFORE implementation starts
- Maintain memory bank for cross-cutting concerns
- Use `[NEEDS CLARIFICATION]` liberally in specs

❌ **Don't:**
- Specify tech stack in initial `/speckit.specify`
- Skip clarification phase
- Mix multiple features in one spec
- Violate constitutional principles (even "just this once")
- Assume AI understands implicit requirements

---

## 3. Brownfield Projects: Incremental SDD Adoption

### 3.1 Ideal Folder Hierarchy - Brownfield

**Strategy**: Add `.specify/` workspace alongside existing structure, **do not refactor existing code initially**.

```
existing-project/                      # Your current codebase (UNCHANGED)
├── src/                               # Existing source code
│   ├── controllers/
│   ├── models/
│   ├── services/
│   └── utils/
│
├── .specify/                          # NEW: Spec Kit workspace
│   ├── memory/
│   │   ├── constitution.md            # NEW: Forward-looking principles
│   │   ├── existing-architecture.md   # DOCUMENT: Current architecture
│   │   ├── migration-strategy.md      # PLAN: Brownfield → SDD transition
│   │   └── tech-debt.md               # TRACK: Known issues & constraints
│   │
│   ├── specs/                         # NEW FEATURES ONLY (initially)
│   │   ├── 001-new-feature-x/         # First SDD-managed feature
│   │   └── 002-new-feature-y/         # Second SDD-managed feature
│   │
│   ├── specs-retro/                   # OPTIONAL: Reverse-engineered specs
│   │   ├── existing-auth-system/      # Spec for existing auth code
│   │   └── existing-payment-flow/     # Spec for existing payment code
│   │
│   └── templates/overrides/
│       └── brownfield-spec.md         # Custom template for brownfield
│
├── .github/prompts/                   # AI agent commands
│   ├── speckit.specify.md
│   ├── speckit.plan.md
│   └── brownfield-reverse.md          # CUSTOM: Reverse engineer existing code
│
└── docs/
    └── sdd-adoption.md                # Track adoption progress
```

### 3.2 Brownfield Adoption Strategy

**Phase 1: Parallel Track (Months 1-3)**
```
Existing Codebase          New Features (SDD)
────────────────────      ─────────────────────
  Unchanged               .specify/specs/001-x/
  Maintained as-is        .specify/specs/002-y/
  Bug fixes only          Full SDD workflow
```

**Phase 2: Selective Reverse Engineering (Months 4-6)**
```bash
# Use Tessl-style reverse engineering
tessl document --code src/auth/login.js

# Or custom brownfield extension
/brownfield.reverse Document existing authentication system in src/auth/

# Creates spec in .specify/specs-retro/auth-system/
# Now can maintain via spec-anchored approach going forward
```

**Phase 3: Incremental Migration (Months 7-12)**
```
High-Value Components:
  Existing → Spec → Refactor (with spec as source of truth)

Low-Value Components:
  Leave as-is (maintain traditionally)

Critical Paths:
  Spec-Anchored for future evolution
```

### 3.3 Brownfield Challenges & Solutions

| Challenge | Solution | Extension/Tool |
|-----------|----------|----------------|
| **Spec-code drift** | Weekly drift detection | `spec-kit-sync` |
| **Existing tests** | Granular migration | `spec-kit-test-migrate` |
| **Team resistance** | Parallel workflows | `spec-kit-hybrid` |
| **Legacy constraints** | Document in constitution | Custom `legacy-constraints.md` |
| **Gradual coverage** | Track coverage metrics | `spec-kit-coverage` |
| **Review burden** | Focus reviews on new specs only | Process change |

### 3.4 Brownfield Best Practices

✅ **Do:**
- Start with NEW features only
- Document existing architecture in memory bank
- Use hybrid workflows (traditional + SDD)
- Track SDD adoption coverage metrics
- Celebrate small wins (first spec-driven feature)
- Allow team to learn gradually

❌ **Don't:**
- Retrofit entire codebase at once
- Force SDD on bug fixes (too small)
- Ignore existing technical debt
- Create specs for code you'll never touch again
- Expect immediate productivity gains

---

## 4. Modern Legacy: Technology Pivots & Modernization

### 4.1 Ideal Folder Hierarchy - Legacy Modernization

**Scenario**: Migrating monolithic Java app to microservices (Node.js + React)

```
legacy-modernization-project/
├── legacy/                            # Original codebase (READ-ONLY)
│   ├── src/                           # Java monolith
│   └── docs/                          # Legacy documentation
│
├── .specify/                          # Modernization workspace
│   ├── memory/
│   │   ├── constitution.md            # Modern architecture principles
│   │   ├── legacy-context.md          # Legacy system understanding
│   │   ├── migration-philosophy.md    # Migration approach
│   │   └── parity-requirements.md     # Feature parity checklist
│   │
│   ├── specs/                         # Feature parity specs
│   │   ├── 001-user-management/       # Spec for legacy User module
│   │   │   ├── spec.md                # Behavior from legacy system
│   │   │   ├── legacy-analysis.md     # Analysis of Java implementation
│   │   │   ├── parity-checklist.md    # Feature-by-feature comparison
│   │   │   ├── plan.md                # Node.js microservice design
│   │   │   └── migration-strategy.md  # Cutover plan
│   │   │
│   │   ├── 002-order-processing/      # Legacy Order module
│   │   └── 003-reporting-engine/      # Legacy Reporting
│   │
│   ├── specs-experiments/             # Experimental specs (what-if scenarios)
│   │   ├── 901-graphql-migration/     # What if we use GraphQL?
│   │   ├── 902-event-sourcing/        # What if we use event sourcing?
│   │   └── 903-serverless/            # What if we go serverless?
│   │
│   └── templates/overrides/
│       ├── legacy-parity-spec.md      # Template for parity specs
│       └── migration-plan.md          # Template for migration planning
│
├── modern/                            # NEW: Modern implementation
│   ├── services/                      # Microservices (generated from specs)
│   │   ├── user-service/              # From spec 001
│   │   ├── order-service/             # From spec 002
│   │   └── reporting-service/         # From spec 003
│   │
│   ├── frontend/                      # React app
│   └── shared/                        # Shared libraries
│
├── migration/                         # Migration tooling
│   ├── data-migration/                # ETL scripts
│   ├── cutover-scripts/               # Deployment automation
│   └── rollback-plans/                # Contingency plans
│
└── docs/
    ├── migration-log.md               # Progress tracking
    └── decision-records/              # Migration ADRs
```

### 4.2 Legacy Modernization Workflow

**Step 1: Legacy Analysis & Spec Creation**
```bash
# Analyze existing behavior
/legacy.analyze Analyze Java User module at legacy/src/com/company/user/

# Create parity spec (documents WHAT the system does)
/speckit.specify Create user management system with exact behavior of legacy User module:
- User registration, authentication, profile management
- Role-based access control (Admin, User, Guest)
- Password reset via email
- Session management
[NEEDS CLARIFICATION: Legacy uses proprietary session store - modern equivalent?]

# Clarify modernization decisions
/speckit.clarify

# Create modern implementation plan
/speckit.plan Microservice architecture:
- Node.js + Express for API
- PostgreSQL (migrate from Oracle)
- Redis for sessions (replace proprietary store)
- JWT for authentication
- Maintain exact API contracts for backwards compatibility
```

**Step 2: Parallel Implementation**
```bash
# Generate modern implementation
/speckit.tasks
/speckit.implement

# Validate parity
/legacy.compare Compare behavior of modern/services/user-service with legacy/src/com/company/user/
```

**Step 3: Incremental Cutover**
```
Phase 1: Read-Only Migration
  Legacy (Write) ←→ Modern (Read + Validate)

Phase 2: Dual-Write
  Legacy (Write) ←→ Modern (Write)
  Compare consistency

Phase 3: Modern Primary
  Legacy (Deprecated) → Modern (Primary)

Phase 4: Decommission
  Legacy (OFF) → Modern (Only)
```

### 4.3 Legacy Modernization Patterns

**Pattern 1: Feature Parity Specs**
```markdown
# spec.md for Legacy Module

## Legacy Behavior (MUST MAINTAIN)
- User login requires username AND email (non-standard)
- Password strength: min 6 chars (weaker than modern standards)
- Sessions expire after 30 days idle (longer than typical)

## Modern Equivalent
- Maintain exact behavior initially (parity requirement)
- Plan future enhancement in separate spec (004-enhanced-auth)

## Migration Risks
- [HIGH] Password hashing algorithm changed (Oracle → bcrypt)
  - Mitigation: One-time rehash on first login
- [MEDIUM] Session store migration (proprietary → Redis)
  - Mitigation: Parallel session validation during cutover
```

**Pattern 2: What-If Experiments**
```bash
# Create experimental specs to evaluate technology pivots
/speckit.specify [EXPERIMENT 901] Redesign order processing as event-sourced system

# Compare implementations
modern/services/order-service/          # Traditional (spec 002)
modern/experiments/order-eventsourced/  # Event-sourced (spec 901)

# Business evaluates based on actual code, not theory
```

**Pattern 3: Strangler Fig Pattern with Specs**
```
Legacy Monolith                 Modern Microservices
┌─────────────────┐            ┌──────────────────┐
│ User Module     │ ────────→  │ User Service     │ (spec 001)
│ Order Module    │ ────────→  │ Order Service    │ (spec 002)
│ Reporting       │            │ [Not migrated]   │
│ Billing         │            │ [Not migrated]   │
└─────────────────┘            └──────────────────┘
        ↓                               ↑
    API Gateway (routes to legacy or modern based on feature)
```

### 4.4 Legacy Modernization Best Practices

✅ **Do:**
- Create parity specs documenting exact legacy behavior
- Use what-if experiments to evaluate technology pivots
- Maintain backwards compatibility in specs
- Track migration risks explicitly
- Parallel implementation for validation
- Incremental cutover with rollback plans

❌ **Don't:**
- Assume you understand all legacy behavior (document it)
- "Improve" behavior during migration (do it separately)
- Big-bang rewrites (too risky)
- Skip parity validation
- Forget to migrate data (not just code)

---

## 5. Transition Across Maturity Levels

### 5.1 Spec-First → Spec-Anchored → Spec-as-Source

```
Spec-First                Spec-Anchored              Spec-as-Source
──────────────            ─────────────────          ──────────────────
Disposable specs          Living specs               Specs ARE source
Code is truth             Specs + Code maintained    Only specs edited
Low commitment            Medium commitment          High commitment
Learning mode             Production mode            Strategic mode

Use for:                  Use for:                   Use for:
- Prototypes              - Production features      - High-churn components
- Experiments             - Documentation required   - Multi-target generation
- Spikes                  - Team collaboration       - Frequent tech pivots
- Learning SDD            - Long-term maintenance    - Non-determinism tolerance
```

### 5.2 Progressive Transition Strategy

**Month 1-3: Spec-First (All Projects)**
```bash
# Goal: Learn SDD workflow, minimal commitment

# Process
/speckit.specify → /speckit.plan → /speckit.implement
→ Ship feature
→ DELETE spec (not anchored)

# Outcome: Team learns spec writing, sees AI generation quality
```

**Month 4-6: Selective Spec-Anchored (Greenfield + High-Value Brownfield)**
```bash
# Goal: Maintain specs for production features

# Process
/speckit.specify → /speckit.plan → /speckit.implement
→ Ship feature
→ KEEP spec in repo
→ Update spec when feature evolves

# Requires
- Spec review in PRs
- Drift detection CI checks
- Spec-code synchronization discipline

# Recommended Extensions
specify extension add spec-kit-sync          # Drift detection
specify extension add spec-kit-reconcile     # Sync specs with code changes
specify extension add spec-kit-ci-guard      # CI validation
```

**Month 7-12: Advanced Spec-Anchored + Experimental Spec-as-Source**
```bash
# Goal: Full lifecycle spec maintenance + selective pure generation

# Spec-Anchored (majority of features)
- Specs maintained by humans and AI
- Code can be manually edited
- Bidirectional sync

# Spec-as-Source (select components only)
// GENERATED FROM SPEC - DO NOT EDIT
// Source: specs/042-payment-processor/spec.md
// To modify, update spec and regenerate

# Criteria for Spec-as-Source:
1. Well-understood domain (low creative variance)
2. Frequent updates needed (high churn)
3. Multiple deployment targets (web + mobile)
4. Strong test coverage (catches generation issues)
5. Team consensus (everyone buys in)
```

### 5.3 Maturity Assessment Matrix

| Indicator | Spec-First Ready | Spec-Anchored Ready | Spec-as-Source Ready |
|-----------|------------------|---------------------|----------------------|
| **Team Skill** | Basic AI prompting | Good spec writing | Expert spec design |
| **Spec Quality** | Conversational | Structured, testable | Precise, unambiguous |
| **Review Culture** | Code review only | Spec + code review | Spec review primary |
| **Tool Maturity** | Basic CLI | Extensions installed | Custom extensions |
| **CI/CD Integration** | None | Drift detection | Full validation pipeline |
| **Documentation Discipline** | Minimal | Maintained | Specs ARE docs |
| **Risk Tolerance** | High (prototypes) | Medium (production) | Low (critical paths) |
| **Change Frequency** | Infrequent | Moderate | Frequent |

### 5.4 Decision Tree: Which Level for This Feature?

```
START
  │
  ├─ Is this a prototype/spike? ──→ YES ──→ Spec-First
  │                               NO
  │                               │
  ├─ Is this production code? ────→ NO ──→ Spec-First
  │                               YES
  │                               │
  ├─ Will this need long-term maintenance? ──→ NO ──→ Spec-First
  │                               YES
  │                               │
  ├─ Do you have spec review bandwidth? ──→ NO ──→ Spec-First (revisit later)
  │                               YES
  │                               │
  ├─ Is documentation required? ──→ NO ──→ Consider Spec-First
  │                               YES
  │                               │
  └─ Spec-Anchored is appropriate
      │
      ├─ Frequent tech stack changes? ──→ YES ──→ Consider Spec-as-Source
      │                                  NO
      │                                  │
      ├─ Low creative variance? ─────────→ NO ──→ Stick with Spec-Anchored
      │                                  YES
      │                                  │
      ├─ Team has expert spec skills? ───→ NO ──→ Stick with Spec-Anchored
      │                                  YES
      │                                  │
      └─ Strong test coverage? ──────────→ YES ──→ Spec-as-Source viable
                                         NO ──→ Stick with Spec-Anchored
```

---

## 6. Enterprise Governance & Compliance

### 6.1 Constitutional Governance Model

**Corporate Constitution (Template)**
```markdown
# [Company Name] Software Development Constitution

## Article I: Security-First Development
All implementations MUST:
1. Follow OWASP Top 10 mitigation strategies
2. Pass automated security scanning before merge
3. Include threat modeling for authentication/authorization features
4. Use approved cryptographic libraries only (see tech-stack.md)

## Article II: Compliance Mandate (SOC2, GDPR, HIPAA)
All features handling:
- PII: MUST implement data encryption at rest and in transit
- Health data: MUST follow HIPAA security controls
- European users: MUST implement GDPR right-to-deletion

## Article III: Observability Requirement
All services MUST:
1. Emit structured logs (JSON format)
2. Expose /health and /metrics endpoints
3. Instrument critical paths with distributed tracing
4. Define SLIs/SLOs in plan.md

## Article IV: Test Coverage Minimums
- Unit tests: ≥80% coverage
- Integration tests: All happy paths + critical error paths
- E2E tests: All user-facing workflows
- Performance tests: All endpoints under expected load
```

### 6.2 Compliance Extension Ecosystem

| Compliance Need | Extension | Purpose |
|----------------|-----------|---------|
| **SOC2** | `spec-kit-soc2` | Enforce SOC2 controls in specs |
| **GDPR** | `spec-kit-gdpr` | PII handling checklist |
| **HIPAA** | `spec-kit-hipaa` | Healthcare data compliance |
| **PCI-DSS** | `spec-kit-pci` | Payment card security |
| **Security** | `spec-kit-security` | OWASP Top 10, SAST integration |
| **Accessibility** | `spec-kit-a11y` | WCAG 2.1 AA compliance |

### 6.3 Enterprise CI/CD Pipeline

```yaml
# .github/workflows/spec-validation.yml

name: Spec-Driven Quality Gates

on:
  pull_request:
    paths:
      - '.specify/specs/**'
      - 'src/**'

jobs:
  spec-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Gate 1: Spec exists for code changes
      - name: Verify Spec Exists
        run: |
          specify extension run spec-kit-ci-guard
          # Fails if code changes without corresponding spec update

      # Gate 2: Constitutional compliance
      - name: Constitutional Validation
        run: |
          specify extension run spec-kit-constitution-check
          # Validates all specs follow Articles I-IX

      # Gate 3: Security review
      - name: Security Compliance Check
        run: |
          specify extension run spec-kit-security
          # Checks for security anti-patterns in specs

      # Gate 4: Spec-code drift detection
      - name: Drift Detection
        run: |
          specify extension run spec-kit-sync --check
          # Fails if implementation diverges from spec

      # Gate 5: Plan review gate (human approval required)
      - name: Plan Review Status
        run: |
          specify extension run spec-kit-plan-review-gate
          # Requires SPEC-APPROVED label on PR
```

---

## 7. Team Organization & Roles

### 7.1 Role Definitions in SDD

| Role | Responsibilities | Skills Required |
|------|------------------|-----------------|
| **Spec Author** | Write feature specs (WHAT/WHY) | Product thinking, domain knowledge, clear writing |
| **Spec Reviewer** | Review specs for completeness | Domain expertise, attention to detail |
| **Plan Architect** | Design technical implementation (HOW) | Architecture, technology evaluation |
| **Task Planner** | Break plans into executable tasks | Decomposition, dependency analysis |
| **Implementation Engineer** | Execute tasks with AI assistance | Traditional dev skills, AI collaboration |
| **Spec Maintainer** | Keep specs synchronized with code | Discipline, process adherence |
| **Constitutional Steward** | Enforce principles, evolve constitution | Principled thinking, change management |

### 7.2 Team Structures

**Small Team (3-5 developers)**
```
All-in-One Model:
- Everyone writes specs, plans, and implements
- Peer review on specs and code
- Rotating constitutional steward
```

**Medium Team (6-15 developers)**
```
Spec-Track + Code-Track Model:
- Spec Track: Product-focused devs (30-40% of team)
  - Write specs, collaborate with product
  - Review plans for feasibility
- Code Track: Implementation-focused devs (60-70%)
  - Create plans from specs
  - Execute implementation
  - Maintain spec-code sync
```

**Large Enterprise (16+ developers)**
```
Specialized Roles:
- Product Engineers (Spec Authors)
- Solution Architects (Plan Architects)
- Feature Teams (Implementation Engineers)
- Platform Team (Constitutional Stewards, Extension Developers)
- Quality Engineering (Spec Reviewers, Drift Detection)
```

---

## 8. Metrics & Success Criteria

### 8.1 Leading Indicators (Early Success Signals)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Spec Clarity** | <5% clarification requests per spec | Track `[NEEDS CLARIFICATION]` removals |
| **Spec Review Time** | <30 min per spec | PR review duration |
| **First-Pass Implementation Success** | >80% of tasks complete without rework | Track task completion vs. revision |
| **Constitutional Compliance** | 100% of specs pass gates | CI/CD validation results |
| **Team Adoption** | >60% of new features use SDD | Feature tracking |

### 8.2 Lagging Indicators (Long-Term Outcomes)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to Feature** | 30-50% reduction vs. baseline | Feature delivery time (spec → production) |
| **Defect Density** | <0.5 defects per KLOC | Post-release bug tracking |
| **Spec-Code Drift** | <10% of features show drift | Weekly drift detection scans |
| **Documentation Coverage** | >90% of features have current specs | Spec coverage analysis |
| **Developer Satisfaction** | >7/10 on SDD workflow | Quarterly surveys |
| **Onboarding Time** | 40-60% reduction | New engineer time to first commit |

### 8.3 Anti-Metrics (What NOT to Optimize For)

❌ **Number of specs created** (focus on quality, not quantity)
❌ **Spec length** (conciseness ≠ quality)
❌ **100% spec-as-source coverage** (wrong goal for most teams)
❌ **Zero human code editing** (spec-anchored allows manual edits)
❌ **Fastest AI generation** (quality > speed)

---

## 9. Risk Mitigation Strategies

### 9.1 Top 10 Enterprise Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **1. Spec Review Burden > Code Review** | High | High | - Invest in spec review tooling<br>- Train team on efficient review<br>- Use preset templates for consistency |
| **2. Spec-Code Drift** | High | Medium | - Automated drift detection (CI)<br>- Bi-weekly sync reviews<br>- `spec-kit-sync` extension |
| **3. Non-Deterministic AI Output** | Medium | High | - Strong test coverage<br>- Constitutional constraints<br>- Code review remains mandatory |
| **4. Team Resistance** | Medium | Medium | - Gradual adoption (spec-first only)<br>- Show early wins<br>- Optional participation initially |
| **5. Tool Immaturity** | Medium | Medium | - Evaluate multiple tools (spec-kit, Kiro, Tessl)<br>- Contribute to open source<br>- Build custom extensions |
| **6. Over-Specification** | Low | High | - Use `[NEEDS CLARIFICATION]` workflow<br>- Clarify ≠ Over-specify<br>- Review for conciseness |
| **7. Under-Specification** | High | Medium | - Constitutional completeness checks<br>- Spec review checklist<br>- Acceptance criteria mandatory |
| **8. Constitutional Violations** | Medium | Low | - Automated gates in CI/CD<br>- Require justification for exceptions<br>- Track complexity budget |
| **9. Brownfield Retrofit Failure** | High | Low | - Start with new features only<br>- Document existing arch first<br>- Hybrid workflows |
| **10. Spec Obsolescence** | Medium | Medium | - Treat specs as code (version control)<br>- Review during feature changes<br>- Deprecation policy |

### 9.2 Contingency Plans

**If Spec-Driven Development Isn't Working After 6 Months:**

**Evaluation Criteria:**
1. Developer satisfaction <5/10
2. Time to feature INCREASED vs. baseline
3. Defect density INCREASED >30%
4. Spec-code drift >30% of features
5. Team actively avoiding SDD workflow

**Contingency Actions:**
1. **Partial Rollback**: Keep specs for documentation only, traditional development
2. **Tool Switch**: Evaluate alternative tools (Kiro, Tessl, custom)
3. **Process Refinement**: Identify specific pain points, address systematically
4. **Skill Gap**: Invest in training (spec writing workshops)
5. **Scope Reduction**: Limit SDD to specific project types (greenfield only)

**Decision Point**: Month 6 retrospective with quantitative data

---

## 10. Quick Start Playbooks

### 10.1 Greenfield Startup Playbook (Day 1)

```bash
# 1. Install
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.0

# 2. Initialize
specify init my-product --ai copilot
cd my-product

# 3. Constitution
/speckit.constitution Create principles for:
- Library-first architecture
- TDD (tests before implementation)
- Max 3 projects initially
- Use Next.js, PostgreSQL, Tailwind

# 4. First Feature
/speckit.specify Build user authentication with email/password
/speckit.clarify
/speckit.plan Use NextAuth.js, Prisma ORM, PostgreSQL
/speckit.tasks
/speckit.implement

# 5. Validate
npm test  # Tests should pass (Article III)
git add .specify/ src/ tests/
git commit -m "feat(001): Add user authentication via SDD"
```

**Time Investment**: 2-4 hours
**Outcome**: Working authentication feature + SDD foundation

---

### 10.2 Brownfield Feature Playbook (Existing Project)

```bash
# 1. Install spec-kit in existing project
cd existing-project
specify init --here --ai copilot

# 2. Document existing architecture
/speckit.constitution Create principles AND document current architecture:
- Existing: Ruby on Rails monolith, PostgreSQL, Redis
- New features: Follow current stack initially
- Future: Consider microservices for high-load features

# 3. First SDD feature (NEW code only)
/speckit.specify Add real-time notifications for order status changes
/speckit.clarify
/speckit.plan Use ActionCable (Rails), Redis pub/sub, React hooks
/speckit.tasks
/speckit.implement

# 4. Integrate with existing code
# - Manually integrate generated service with existing Order model
# - Update existing OrdersController to trigger notifications
# - Keep spec for future maintenance

# 5. Validate
rails test
git add .specify/ app/services/notifications/ spec/services/notifications/
git commit -m "feat(001): Add real-time order notifications"
```

**Time Investment**: 3-6 hours (includes integration work)
**Outcome**: New feature integrated with existing codebase + SDD learning

---

### 10.3 Legacy Modernization Playbook (Migration Project)

```bash
# 1. Dual repository setup
mkdir legacy-to-modern && cd legacy-to-modern
specify init modern-platform --ai copilot
cd modern-platform

# 2. Constitution with migration focus
/speckit.constitution Create principles for legacy migration:
- Feature parity is MANDATORY initially
- Maintain exact API contracts during transition
- Incremental cutover (strangler fig pattern)
- Document legacy behavior explicitly in specs

# 3. Analyze first legacy module
/legacy.analyze Analyze legacy Java User module behavior from ../legacy-app/src/user/

# 4. Create parity spec
/speckit.specify Build user management service with exact behavior of legacy system:
[Paste legacy analysis results]
- Maintain non-standard login flow (username + email required)
- Support legacy session format during migration
- Provide REST API matching legacy endpoints

# 5. Modern implementation
/speckit.plan Node.js + Express, PostgreSQL, Redis
/speckit.tasks
/speckit.implement

# 6. Parity validation
/legacy.compare Compare modern/user-service with legacy User module
# Generates test suite validating behavior match

# 7. Deploy parallel (Phase 1: Read-Only)
# - Legacy writes, modern reads and validates
# - Compare outputs, track discrepancies
```

**Time Investment**: 1-2 weeks per module
**Outcome**: Modern equivalent with proven parity + incremental migration path

---

## 11. Conclusion & Next Steps

### 11.1 Key Takeaways

1. **SDD is a paradigm shift**, not just a productivity tool
2. **Progressive adoption** is safer than all-in commitment
3. **Greenfield adoption** is easiest, **brownfield** requires discipline, **legacy** needs careful planning
4. **Constitutional principles** prevent common pitfalls
5. **Spec review culture** is as important as code review
6. **Tool ecosystem** is experimental but rapidly maturing
7. **Team buy-in** is critical to success

### 11.2 Recommended Adoption Path

**Month 1:**
- Install spec-kit and complete tutorial
- 1-2 greenfield spikes (spec-first, disposable)
- Team training on constitutional principles
- Evaluate tool fit (spec-kit vs. Kiro vs. Tessl)

**Month 2-3:**
- First production feature with spec-anchored
- Establish spec review practices
- Install essential extensions (ci-guard, sync)
- Measure time/quality impact

**Month 4-6:**
- Scale to 50% of new features
- Introduce brownfield features
- Develop custom extensions for enterprise needs
- Quarterly metrics review

**Month 7-12:**
- Evaluate spec-as-source for select components
- Legacy modernization pilot (if applicable)
- Full CI/CD integration
- Enterprise governance model

**Year 2+:**
- Advanced workflows (MAQA, Fleet)
- Custom constitutional presets
- Cross-team spec standards
- Community contributions

### 11.3 Resources

**Official Documentation:**
- spec-kit: https://github.com/github/spec-kit
- Community Extensions: https://speckit-community.github.io/extensions/
- Martin Fowler Analysis: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html

**Enterprise Support:**
- GitHub Professional Services (for spec-kit)
- Community Slack/Discord channels
- Internal champions network

**Training:**
- Spec writing workshops
- Constitutional design sessions
- Tool-specific certifications (coming soon)

---

**Document Version:** 1.0
**Last Updated:** April 24, 2026
**Maintained By:** Enterprise Architecture Team
**Review Cycle:** Quarterly
